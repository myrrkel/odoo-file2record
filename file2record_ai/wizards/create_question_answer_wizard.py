# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class CreateQuestionAnswerWizard(models.TransientModel):
    _inherit = 'create.question.answer.wizard'

    answer_type = fields.Selection(selection_add=[('record_values', 'Record Values')])

    def get_completion_answer(self, completion_result_id):
        if self.answer_type == 'record_values':
            return completion_result_id.get_answer_with_record_values()
        return super(CreateQuestionAnswerWizard, self).get_completion_answer(completion_result_id)

