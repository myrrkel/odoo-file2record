# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class UploadFileConfig(models.Model):
    _inherit = 'file2record.config'

    def _get_record_creation_method_list(self):
        res = super(UploadFileConfig, self)._get_record_creation_method_list()
        res.append(('ai', _('AI Completion')))
        return res

    record_creation_method = fields.Selection(selection=_get_record_creation_method_list)
    ai_completion_id = fields.Many2one('ai.completion', string='AI Completion')
    additional_instructions = fields.Text()
