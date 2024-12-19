# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, _, api
from odoo.osv import expression
import logging
_logger = logging.getLogger(__name__)


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    # @api.model
    # def _get_json_model_one2many_field_description(self):
    #     product_template_id = self.env['product.template']._get_json_model_many2one_field_description()
    #     return {'name': '', 'product_uom_qty': 0, 'price_unit': 0, 'tax_rate': 0,
    #             'product_template_id': product_template_id,
    #             }
    # @api.model
    # def _create_one2many_record(self, values_list):
    #     res = super(HrExpense, self)._create_one2many_record(values_list)
    #     return res
    #
    # def _get_json_model_fields_description(self):
    #     res = super(HrExpense, self)._get_json_model_fields_description()
    #     return res
    #
    # def _get_fields_description(self, json_dict):
    #     res = super(HrExpense, self)._get_fields_description(json_dict)
    #     return res

    def create_expense_from_attachments(self, attachment_ids=None, view_type='list'):
        return self.create_records_from_attachments(attachment_ids)
