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

    def field_value_to_ai_answer_value(self, field_name):
        field = self._fields[field_name]
        if field.type == 'many2one':
            if field.comodel_name == 'attribute.option':
                return {'option_value': self[field_name].name}
        return super(ProductTemplate, self).field_value_to_ai_answer_value(field_name)

    def model_description_excluded_fields(self):
        res = super(ProductTemplate, self).model_description_excluded_fields()
        fields = [
            'attribute_set_completion_rate',
            'sequence',
            'sale_ok',
            'purchase_ok',
            'active',
            'color',
            'can_image_1024_be_zoomed',
            'has_configurable_attributes',
            'sale_line_warn_msg',
        ]
        res.extend(fields)
        return res
