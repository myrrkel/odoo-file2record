# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, _, api
import logging
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _get_field_description(self, field):
        res = super(ProductTemplate, self)._get_field_description(field)
        if field.comodel_name == 'attribute.option':
            model_id = self.env['ir.model.fields'].search([('model', '=', self._name), ('name', '=', field.name)])
            attribute_id = self.env['attribute.attribute'].search([('field_id', '=', model_id.id)])
            available_options = ', '.join(attribute_id.option_ids.mapped('name'))
            res += f'\n    Available {field.name} values : {available_options}'
        return res
