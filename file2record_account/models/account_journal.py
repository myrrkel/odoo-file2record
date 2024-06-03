# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, _, api
from odoo.osv import expression
import logging
_logger = logging.getLogger(__name__)


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    def create_document_from_attachment(self, attachment_ids=None):
        res = self.env['account.move'].create_records_from_attachments(attachment_ids)
        return res
