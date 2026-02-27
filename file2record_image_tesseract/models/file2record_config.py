# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields
import ast
import logging

_logger = logging.getLogger(__name__)


class UploadFileConfig(models.Model):
    _inherit = 'file2record.config'

    tesseract_parameters = fields.Char()
    preprocess_with_osd = fields.Boolean()
    get_lang_from_ai = fields.Boolean("Get Language From AI")

    def get_tesseract_params(self):
        return ast.literal_eval(self.tesseract_parameters) if self.tesseract_parameters else {}
