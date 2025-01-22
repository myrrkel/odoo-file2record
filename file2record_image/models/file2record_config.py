# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields, api, _
import logging
import ast

_logger = logging.getLogger(__name__)


class UploadFileConfig(models.Model):
    _inherit = 'file2record.config'

    def _get_data_type_list(self):
        res = super(UploadFileConfig, self)._get_data_type_list()
        res.append(('image', _('Image')))
        return res

    data_type = fields.Selection(selection=_get_data_type_list)
    tesseract_parameters = fields.Char()
    preprocess_with_osd = fields.Boolean()
    get_lang_from_ai = fields.Boolean()

    def get_tesseract_params(self):
        return ast.literal_eval(self.tesseract_parameters) if self.tesseract_parameters else {}