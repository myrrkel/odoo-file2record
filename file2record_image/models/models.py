# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models
from odoo.tools import html2plaintext
import io
from PIL import Image
from pillow_heif import register_heif_opener
import pytesseract
import logging
import fitz
from .image_processing import transform_image
_logger = logging.getLogger(__name__)

register_heif_opener()

class BaseModel(models.AbstractModel):
    _inherit = 'base'

    def get_text_from_image(self, content):
        config_id = self.get_file2record_config('image')
        params = config_id.get_tesseract_params() if config_id else {'config': '--psm 6'}
        img = Image.open(io.BytesIO(content))

        if config_id and config_id.preprocess_with_osd:
            image_osd = self.get_tesseract_image_osd(img)
            if image_osd.get('rotate'):
                if image_osd['rotate'] != 180 and image_osd.get('orientation_conf') >= 0.5:
                    img = img.rotate(360 - image_osd['rotate'], expand=True)

            if config_id and config_id.get_lang_from_ai:
                text = pytesseract.image_to_string(img, timeout=10)
                prompt = self.get_guess_language_prompt(text)
                lang = config_id.ai_completion_id.create_completion(prompt=prompt)
                if lang:
                    params['lang'] = lang

        return self.get_ocr_text(img, params=params)

    def _is_attachment_image(self, attachment_id):
        extension = attachment_id.name.lower().split('.')[-1]
        return 'image' in attachment_id.mimetype or extension in ['jpg', 'png', 'jpeg', 'heic']

    def get_guess_language_prompt(self, text):
        languages = ','.join(pytesseract.get_languages(config=''))
        prompt = ('Return the language code corresponding to the following document.\n'
                  'If the document is not in a known language, return an empty string.\n'
                  'Available languages: %s\n\n'
                  '#DOCUMENT \n%s') % (languages, text)
        return prompt

    def get_tesseract_image_osd(self, img, retry=False, transformed=False, config=''):
        image_osd = {}
        try:
            image_osd = pytesseract.image_to_osd(img, output_type=pytesseract.Output.DICT, config=config)
        except Exception as e:
            if not retry:
                if not transformed:
                    img = transform_image(img, size_ratio=3)

                rotated_img = img.rotate(-90, expand=True)
                left_image_osd = self.get_tesseract_image_osd(rotated_img, retry=True, transformed=True, config=config)
                rotated_img = img.rotate(90, expand=True)
                right_image_osd = self.get_tesseract_image_osd(rotated_img, retry=True, transformed=True, config=config)
                if left_image_osd['orientation_conf'] > right_image_osd['orientation_conf']:
                    image_osd = left_image_osd
                    image_osd['rotate'] = image_osd['rotate'] + 90
                else:
                    image_osd = right_image_osd
                    image_osd['rotate'] = image_osd['rotate'] - 90

            if image_osd:
                _logger.info('Image OSD (Retry) : %s' % image_osd)
                return image_osd
            else:
                _logger.warning(e)
                pass
        _logger.info('Image OSD : %s', image_osd)
        return image_osd

    def _get_values_from_attachment(self, attachment_id, content):
        if self._is_attachment_image(attachment_id):
            config_id = self.get_file2record_config('image')
            if config_id and config_id.ocr_completion_id:
                text = config_id.ocr_completion_id.create_completion(attachment_id.id,
                                                                      prompt='get text with OCR')
            else:
                text = self.get_text_from_image(content)
                _logger.info('OCR Result : %s', text)
            res = self._get_record_values(attachment_id.name, 'image', text.strip())
            if len(res.keys()) <= 1 or res.get('file_processing_error', False):
                text = self.get_retry_ocr_text(Image.open(io.BytesIO(content)), params={'config': '--psm 6'})
                _logger.info('OCR Retry')
                res = self._get_record_values(attachment_id.name, 'image', text.strip())
                _logger.info('OCR Retry Result : %s', text)
                if len(res.keys()) <= 1 or res.get('file_processing_error', False):
                    config_id = self.get_file2record_config('image')
                    if hasattr(config_id, 'retry_ocr_completion_id') and config_id.retry_ocr_completion_id:
                        _logger.info('OCR Retry #2')
                        text = config_id.retry_ocr_completion_id.create_completion(attachment_id.id,
                                                                                   prompt='get text with OCR')
                        _logger.info('OCR Retry #2 Result : %s', text)
                        res = self._get_record_values(attachment_id.name, 'image', text.strip())
            return res

        return super(BaseModel, self)._get_values_from_attachment(attachment_id, content)

    def _get_ocr_text(self, img, timeout=10, params=None):
        if params is None:
            params = {}
        try:
            return pytesseract.image_to_string(img, timeout=timeout, **params)
        except Exception as err:
            _logger.error(err, exc_info=True)
            pass
            return ''

    def get_ocr_text(self, img, timeout=10, params=None):
        ocr_image = transform_image(img, size_ratio=2, adaptive_sharpening=True, median_filter=False, contrast=1,
                            revert_resize=False)

        return self._get_ocr_text(ocr_image, timeout=timeout, params=params)

    def get_retry_ocr_text(self, img, timeout=10, params=None):
        ocr_image = transform_image(img, size_ratio=0.5, adaptive_sharpening=True, median_filter=True, contrast=2)
        return self._get_ocr_text(ocr_image, timeout=timeout, params=params)

    def get_mixed_ocr_text(self, img, timeout=10, params=None):
        if params is None:
            params = {}
        text = self._get_ocr_text(img, timeout=timeout, params=params)
        alternative_image = transform_image(img, size_ratio=2, revert_resize=False,
                                            adaptive_sharpening=True, median_filter=True, contrast=2)
        alternative_text = self._get_ocr_text(alternative_image, timeout=timeout, params=params)
        return f'ORIGINAL OCR :\n\n {text}\n\nALTERNATIVE OCR : \n\n{alternative_text}'''

    def _get_record_values_from_content(self, name, content_type, content):
        if content_type == 'image':
            return self._get_record_values_from_text(name, content)
        return super(BaseModel, self)._get_record_values_from_content(name, content_type, content)

    def _get_html_from_pdf(self, content, drop_last_page=False):
        res = super(BaseModel, self)._get_html_from_pdf(content, drop_last_page=drop_last_page)
        if html2plaintext(res):
            return res

        doc = fitz.open("pdf", content)
        pdf_img_list = []
        img_txt_list = []
        for i, page in enumerate(doc):
            page.read_contents()
            img_list = page.get_images()
            for img in img_list:
                try:
                    pdf_img_list.append(doc.extract_image(img[0]))
                except Exception as err:
                    _logger.warning(err, exc_info=True)
                    pass
        if not pdf_img_list:
            return ''
        for pdf_img in pdf_img_list:
            try:
                img_txt = self.get_text_from_image(pdf_img['image'])
                # img_txt = self.get_ocr_text(Image.open(io.BytesIO(pdf_img['image'])), params=params)
                _logger.info('PDF Image OCR Result : %s', img_txt)
                if img_txt:
                    img_txt_list.append(img_txt)
            except Exception as err:
                _logger.warning(err, exc_info=True)
                pass
        return '\n'.join(img_txt_list)
