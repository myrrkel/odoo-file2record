# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class UploadFileConfig(models.Model):
    _inherit = 'file2record.config'

    show_upload_camera_button = fields.Boolean(default=False)

    @api.model
    def is_camera_to_record_button_visible(self, model):
        if self.search([('model', '=', model), ('show_upload_camera_button', '=', True)]):
            return True
