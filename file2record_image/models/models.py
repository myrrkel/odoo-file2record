# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models
from odoo.tools import html2plaintext
import io
from PIL import Image
from pillow_heif import register_heif_opener
import logging
import fitz

_logger = logging.getLogger(__name__)

register_heif_opener()


class BaseModel(models.AbstractModel):
    _inherit = 'base'

    def get_text_from_image(self, content, attachment_id=None):
        config_id = self.get_file2record_config('image')
        if attachment_id and config_id.ocr_completion_id:
            return config_id.ocr_completion_id.create_completion(attachment_id.id, self._ocr_prompt())
        return ''

    def _is_attachment_image(self, attachment_id):
        extension = attachment_id.name.lower().split('.')[-1]
        return 'image' in attachment_id.mimetype or extension in ['jpg', 'png', 'jpeg', 'heic']

    def _ocr_prompt(self):
        return 'Return the text of the document.'

    def _get_values_from_attachment(self, attachment_id, content):
        if self._is_attachment_image(attachment_id):
            text = self.get_text_from_image(content, attachment_id)
            _logger.info('OCR Result : %s', text)
            res = self._get_record_values(attachment_id.name, 'image', text.strip())
            return res

        return super(BaseModel, self)._get_values_from_attachment(attachment_id, content)

    def _get_record_values_from_content(self, name, content_type, content):
        if content_type == 'image':
            return self._get_record_values_from_text(name, content)
        return super(BaseModel, self)._get_record_values_from_content(name, content_type, content)

    def _get_html_from_pdf(self, content, drop_last_page=False):
        res = super(BaseModel, self)._get_html_from_pdf(content, drop_last_page=drop_last_page)
        if html2plaintext(res):
            return res

        try:
            if not content or not isinstance(content, bytes):
                _logger.error("Invalid PDF content: content must be non-empty bytes")
                return ''

            doc = fitz.open("pdf", content)

            if doc.page_count <= 0:
                _logger.error("Invalid PDF document: no pages found")
                doc.close()
                return ''

        except Exception as e:
            _logger.error(f"Failed to open PDF document: {e}", exc_info=True)
            return ''

        pdf_img_list = []
        img_txt_list = []
        try:
            for i, page in enumerate(doc):
                page.read_contents()
                img_list = page.get_images()
                for img in img_list:
                    try:
                        pdf_img_list.append(doc.extract_image(img[0]))
                    except Exception as err:
                        _logger.warning(err, exc_info=True)
                        pass
        except Exception as e:
            _logger.error(f"Error processing PDF pages: {e}", exc_info=True)
            doc.close()
            return ''
        finally:
            doc.close()

        if not pdf_img_list:
            return ''
        for pdf_img in pdf_img_list:
            try:
                img_txt = self.get_text_from_image(pdf_img['image'])
                _logger.info('PDF Image OCR Result : %s', img_txt)
                if img_txt:
                    img_txt_list.append(img_txt)
            except Exception as err:
                _logger.warning(err, exc_info=True)
                pass
        return '\n'.join(img_txt_list)
