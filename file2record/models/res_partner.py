# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, _, api
from odoo.osv import expression
import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _get_json_model_many2one_field_description(self):
        return {'name': '', 'phone': '', 'email': '',
                'street': '', 'city': '', 'zip': '',
                'country_id': self.env['res.country']._get_json_model_many2one_field_description(),
                'is_company': False,
                'company_name': '',
                }
    def _find_or_create_many2one_domain(self, values):
        domain = []
        if values.get('email'):
            domain.append([('email', '=', values['email'])])
        if values.get('phone'):
            domain.append([('phone', '=', values['phone'])])
        if values.get('mobile'):
            domain.append([('mobile', '=', values['mobile'])])
        if len(domain) > 1:
            domain = expression.OR(domain)
        else:
            domain = domain[0] if domain else []
        domain_address = []
        if values.get('name'):
            domain_address.append([('name', 'ilike', values['name'])])
            if values.get('street'):
                domain_address.append([('street', 'ilike', values['street'])])
            if len(domain_address) > 1:
                domain_address = expression.AND(domain_address)
            domain_city = []
            if values.get('city'):
                domain_city.append([('city', 'ilike', values['city'])])
            if values.get('zip'):
                domain_city.append([('zip', 'ilike', values['zip'])])
            if len(domain_city) > 1:
                domain_city = expression.OR(domain_city)
            else:
                domain_city = domain_city[0] if domain_city else []
            if domain_address and domain_city:
                domain_address = expression.AND([domain_address, domain_city])

        if domain and domain_address:
            return expression.OR([domain, domain_address])
        if domain_address:
            return domain_address
        return domain

    def _find_or_create_many2one_record(self, values):
        if not values.get('name'):
            return
        if 'active' in values:
            values['active'] = True
        res = super(ResPartner, self)._find_or_create_many2one_record(values)
        if not res:
            if values.get('country_id'):
                country_id = self.env['res.country']._find_or_create_many2one_record(values['country_id'])
                if country_id:
                    values['country_id'] = country_id
                else:
                    values.pop('country_id')
            rec_id = self.create(values)
            return rec_id.id
        return res

    def cleanup_record_values(self, values):
        if 'active' in values:
            values.pop('active')
        return super(ResPartner, self).cleanup_record_values(values)
