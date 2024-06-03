# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, _, api
import io
from PIL import Image
import pytesseract
import logging
_logger = logging.getLogger(__name__)


class BaseModel(models.AbstractModel):
    _inherit = 'base'

    def _is_attachment_image(self, attachment_id):
        extension = attachment_id.name.lower().split('.')[-1]
        return 'image' in attachment_id.mimetype or extension in ['jpg', 'png']

    def _get_values_from_attachment(self, attachment_id, content):
        if self._is_attachment_image(attachment_id):
            img = Image.open(io.BytesIO(content))
            text = pytesseract.image_to_string(img, timeout=10)
            # text = pytesseract.image_to_alto_xml(img)
            _logger.info(text)
            return self._get_record_values(attachment_id.name, 'image', text.strip())

        return super(BaseModel, self)._get_values_from_attachment(attachment_id, content)

    def _get_record_values_from_content(self, name, content_type, content):
        if content_type == 'image':
            return self._get_record_values_from_text(name, content)
        return super(BaseModel, self)._get_record_values_from_content(name, content_type, content)

