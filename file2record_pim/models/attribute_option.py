# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, _, api
import logging
_logger = logging.getLogger(__name__)


class AttributeOption(models.Model):
    _inherit = 'attribute.option'

    @api.model
    def _get_json_model_many2one_field_description(self):
        return {'option_value': ''}

    def _find_or_create_many2one_domain(self, values):
        domain = []
        if values.get('option_value'):
            domain.append(('name', '=', values['option_value']))
        if self.env.context.get('field_name'):
            domain.append(('attribute_id.name', '=', self.env.context.get('field_name')))
        return domain
