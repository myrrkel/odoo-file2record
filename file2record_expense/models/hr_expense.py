# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, _, api
from odoo.osv import expression
import logging
_logger = logging.getLogger(__name__)


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    def create_expense_from_attachments(self, attachment_ids=None, view_type='list'):
        return self.create_records_from_attachments(attachment_ids)
