# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models
import io
from PIL import Image
import pytesseract
import logging
from odoo.tools import image_to_base64
from .image_processing import transform_image
_logger = logging.getLogger(__name__)


class BaseModel(models.AbstractModel):
    _inherit = 'base'

    def _is_attachment_image(self, attachment_id):
        extension = attachment_id.name.lower().split('.')[-1]
        return 'image' in attachment_id.mimetype or extension in ['jpg', 'png']

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
        except pytesseract.TesseractError as e:
            if not retry and 'Invalid resolution' in e.message:
                if not transformed:
                    img = transform_image(img, size_ratio=2, adaptive_sharpening=True, median_filter=True,
                                                      contrast=2)
                for rotate in [0, 90, 180, 270]:
                    rotated_img = img.rotate(rotate, expand=True)
                    image_osd = self.get_tesseract_image_osd(rotated_img, retry=True, transformed=True, config=config)
                    if image_osd:
                        image_osd['rotate'] = rotate
                        _logger.info('Image OSD (Rotated %s) : %s' % (rotate, image_osd))
                        return image_osd
            else:
                _logger.error(e.message)
                pass
        except Exception as e:
            _logger.error(e)
            pass
        _logger.info('Image OSD : %s', image_osd)
        return image_osd

    def _get_values_from_attachment(self, attachment_id, content):
        if self._is_attachment_image(attachment_id):
            config_id = self.get_file2record_config('image')
            params = config_id.get_tesseract_params()
            img = Image.open(io.BytesIO(content))
            image_osd = {}
            if config_id and config_id.preprocess_with_osd:
                image_osd = self.get_tesseract_image_osd(img)
                if image_osd.get('rotate') and image_osd.get('orientation_conf') >= 0.5:
                    img = img.rotate(360 - image_osd['rotate'], expand=True)

                if config_id and config_id.get_lang_from_ai:
                    text = pytesseract.image_to_string(img, timeout=10)
                    prompt = self.get_guess_language_prompt(text)
                    lang = config_id.ai_completion_id.create_completion(prompt=prompt)
                    if lang:
                        params['lang'] = lang

            text = self.get_ocr_text(img, params=params)
            _logger.info('OCR Result : %s', text)
            res = self._get_record_values(attachment_id.name, 'image', text.strip())
            if len(res.keys()) <= 1 and params:
                retry_img = img.rotate(-90, expand=True) if not image_osd else img
                text = self.get_retry_ocr_text(retry_img, params=params)
                _logger.info('OCR Retry : %s', text)
                res = self._get_record_values(attachment_id.name, 'image', text.strip())
                res['retry'] = True

            if len(res.keys()) > 1 and image_osd.get('rotate') and image_osd.get('orientation_conf') >= 0.5:
                attachment_id.datas = image_to_base64(img, 'PNG')
            return res

        return super(BaseModel, self)._get_values_from_attachment(attachment_id, content)

    def get_ocr_text(self, img, timeout=10, params=None):
        if params is None:
            params = {}
        ocr_image = transform_image(img, size_ratio=2, adaptive_sharpening=True, median_filter=True, contrast=3,
                            revert_resize=False)
        text = pytesseract.image_to_string(ocr_image, timeout=timeout, **params)
        return text

    def get_retry_ocr_text(self, img, timeout=10, params=None):
        if params is None:
            params = {}
        ocr_image = transform_image(img, size_ratio=1, adaptive_sharpening=True, median_filter=False, contrast=2)
        text = pytesseract.image_to_string(ocr_image, timeout=timeout, **params)
        return text

    def get_mixed_ocr_text(self, img, timeout=10, params=None):
        if params is None:
            params = {}
        text = pytesseract.image_to_string(img, timeout=timeout, **params)
        alternative_image = transform_image(img, size_ratio=2, revert_resize=False,
                                            adaptive_sharpening=True, median_filter=True, contrast=2)
        alternative_text = pytesseract.image_to_string(alternative_image, timeout=timeout)
        return f'ORIGINAL OCR :\n\n {text}\n\nALTERNATIVE OCR : \n\n{alternative_text}'''

    def _get_record_values_from_content(self, name, content_type, content):
        if content_type == 'image':
            return self._get_record_values_from_text(name, content)
        return super(BaseModel, self)._get_record_values_from_content(name, content_type, content)
