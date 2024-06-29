# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
import json
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class AICompletionResult(models.Model):
    _inherit = 'ai.completion.result'

    def get_answer_with_record_values(self):
        if not self.model == 'ir.attachment':
            raise UserError(_("Model %s is not supported") % self.model)
        values = json.loads(self.answer)
        attachment_id = self.resource_ref
        rec = self.env[attachment_id.res_model].browse(attachment_id.res_id)
        if not rec:
            return self.answer
        for key in values.keys():
            if key in rec.model_description_excluded_fields():
                continue
            if hasattr(rec, key):
                values[key] = rec.field_value_to_ai_answer_value(key)
        return json.dumps(values, indent=2, ensure_ascii=False)

    def get_completion_answer(self, answer_type):
        if answer_type == 'record_values':
            return self.get_answer_with_record_values()
        return super(AICompletionResult, self).get_completion_answer(answer_type)
