# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class UploadFileConfig(models.Model):
    _inherit = 'file2record.config'

    def _get_data_type_list(self):
        res = super(UploadFileConfig, self)._get_data_type_list()
        res.append(('image', _('Image')))
        return res

    data_type = fields.Selection(selection=_get_data_type_list)
