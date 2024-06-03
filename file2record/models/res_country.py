# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, _, api
from odoo.osv import expression
import logging
_logger = logging.getLogger(__name__)


class ResCountry(models.Model):
    _inherit = 'res.country'

    @api.model
    def _get_json_model_many2one_field_description(self):
        return {'name': '', 'code': ''}

    def _find_or_create_many2one_domain(self, values):
        domain = []
        if values.get('name'):
            domain.append([('name', '=', values['name'])])
        if values.get('code'):
            domain.append([('code', '=', values['code'])])
        if len(domain) > 1:
            domain = expression.OR(domain)
        return domain
