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
    default_record_creation_prompt = fields.Text(compute='_compute_default_record_creation_prompt')
    is_default_ai_completion = fields.Boolean(compute='_compute_is_default_ai_completion')

    def _compute_is_default_ai_completion(self):
        default_completion_id = self.env.ref('file2record_ai.default_record_creation')
        for rec in self:
                rec.is_default_ai_completion = rec.ai_completion_id == default_completion_id


    def _compute_default_record_creation_prompt(self):
        for rec in self:
            m_model = self.env[rec.model].with_context(file2record_config_id=rec.id)
            prompt = m_model._get_default_record_creation_prompt('', rec.additional_instructions)
            rec.default_record_creation_prompt = prompt
