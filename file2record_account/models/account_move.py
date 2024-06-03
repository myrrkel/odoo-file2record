# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, _, api
from odoo.osv import expression
import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _create_record_from_attachment(self, res_id):
        res = super(AccountMove, self)._create_record_from_attachment(res_id)
        res.with_context(no_new_invoice=True).message_post(attachment_ids=[res_id])
        return res
