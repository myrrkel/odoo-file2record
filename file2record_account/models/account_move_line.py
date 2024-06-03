# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, _, api
from odoo.osv import expression
import logging
_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.model
    def _get_json_model_one2many_field_description(self):
        product_template_id = self.env['product.template']._get_json_model_many2one_field_description()
        return {'name': '', 'quantity': 0, 'price_unit': 0, 'tax_rate': 0,
                'product_template_id': product_template_id,
                }
    @api.model
    def _create_one2many_record(self, values_list):
        for values in values_list:
            if values.get('name') and values.get('product_template_id'):
                if not values['product_template_id'].get('name'):
                    values['product_template_id']['name'] = values['name']
            if values.get('product_template_id'):
                values['product_template_id'] = self.env['product.template']._find_or_create_many2one_record(values.get('product_template_id'))
        res = super(AccountMoveLine, self)._create_one2many_record(values_list)
        for values in res:
            product_template_id = values['product_template_id']
            if not values.get('product_id') and product_template_id:
                domain = [('product_tmpl_id', '=', product_template_id)]
                product_id = self.env['product.product'].search(domain, limit=1)
                values['product_id'] = product_id.id
                values.pop('product_template_id')
            if not values.get('tax_ids'):
                amount = 0
                if values.get('tax_rate'):
                    amount = values['tax_rate']
                    values.pop('tax_rate')
                tax = self.env['account.tax'].search([
                    ('company_id', '=', self.env.user.company_id.id),
                    ('amount', '=', amount),
                    ('amount_type', '=', 'percent'),
                    ('type_tax_use', '=', 'sale'),
                ], limit=1)
                if tax:
                    values['tax_id'] = tax.ids

        return res

    def _get_fields_description(self, json_dict):
        res = super(AccountMoveLine, self)._get_fields_description(json_dict)
        res += '\ntax_rate (float) : tax rate in percent'
        return res
