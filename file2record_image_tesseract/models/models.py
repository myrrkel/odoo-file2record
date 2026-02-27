# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models
import io
from PIL import Image
import pytesseract
import logging

_logger = logging.getLogger(__name__)


class BaseModel(models.AbstractModel):
    _inherit = 'base'

    def get_text_from_image(self, content, attachment_id=None):
        config_id = self.get_file2record_config('image')
        if attachment_id and config_id.ocr_completion_id and not config_id.tesseract_parameters:
            return config_id.ocr_completion_id.create_completion(attachment_id.id, self._ocr_prompt())
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

    def get_guess_language_prompt(self, text):
        languages = ','.join(pytesseract.get_languages(config=''))
        prompt = ('Return the language code corresponding to the following document.\n'
                  'If the document is not in a known language, return an empty string.\n'
                  'Available languages: %s\n\n'
                  '#DOCUMENT \n%s') % (languages, text)
        return prompt

    def get_tesseract_image_osd(self, img, retry=False, transformed=False, config=''):
        from file2record_image.models.image_processing import transform_image
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
        from file2record_image.models.image_processing import transform_image
        ocr_image = transform_image(img, size_ratio=2, adaptive_sharpening=True, median_filter=False, contrast=1,
                            revert_resize=False)

        return self._get_ocr_text(ocr_image, timeout=timeout, params=params)

    def get_retry_ocr_text(self, img, timeout=10, params=None):
        from file2record_image.models.image_processing import transform_image
        ocr_image = transform_image(img, size_ratio=0.5, adaptive_sharpening=True, median_filter=True, contrast=2)
        return self._get_ocr_text(ocr_image, timeout=timeout, params=params)

    def get_mixed_ocr_text(self, img, timeout=10, params=None):
        from file2record_image.models.image_processing import transform_image
        if params is None:
            params = {}
        text = self._get_ocr_text(img, timeout=timeout, params=params)
        alternative_image = transform_image(img, size_ratio=2, revert_resize=False,
                                            adaptive_sharpening=True, median_filter=True, contrast=2)
        alternative_text = self._get_ocr_text(alternative_image, timeout=timeout, params=params)
        return f'ORIGINAL OCR :\n\n {text}\n\nALTERNATIVE OCR : \n\n{alternative_text}'
