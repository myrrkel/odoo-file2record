# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, _, api
from odoo.osv import expression
import logging
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def _get_json_model_many2one_field_description(self):
        return {'name': '', 'default_code': '', 'list_price': 0}

    def _find_or_create_many2one_domain(self, values):
        domain = []
        if values.get('name'):
            domain.append([('name', 'ilike', values['name'])])
        if values.get('default_code'):
            domain.append([('default_code', 'ilike', values['default_code'])])
        if len(domain) > 1:
            domain = expression.OR(domain)
        else:
            domain = domain[0] if domain else []
        return domain

    def _find_or_create_many2one_record(self, values):
        res = super(ProductTemplate, self)._find_or_create_many2one_record(values)
        if not res:
            rec_id = self.create(values)
            return rec_id.id
        return res

    def _get_fields_description(self, json_dict):
        res = super(ProductTemplate, self)._get_fields_description(json_dict)
        res += '\n tax_rate (float) : tax rate in percent'
        return res
