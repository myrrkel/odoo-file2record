# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, _, api
import json
import logging
_logger = logging.getLogger(__name__)


class BaseModel(models.AbstractModel):
    _inherit = 'base'

    def _get_record_values_from_content(self, name, content_type, content):
        config_id = self.get_file2record_config(content_type)
        if config_id.record_creation_method == 'ai':
            completion_id = config_id.ai_completion_id
            prompt = '%s \n %s' % (completion_id.get_prompt(), content)
            # res = completion_id.create_completion(prompt=prompt)
            # return json.loads(res[0])
            return {'email_normalized': 'antoine@teremis.fr', 'message_bounce': 0, 'name': 'Antoine NEBOUT', 'display_name': 'Antoine NEBOUT', 'parent_id': {'name': False, 'phone': False, 'email': False, 'street': False, 'city': False, 'zip': False, 'country_id': {'name': False, 'code': False}, 'is_company': False, 'company_name': False}, 'ref': False, 'vat': False, 'company_registry': False, 'website': False, 'comment': False, 'active': False, 'employee': False, 'function': False, 'street': '16d Charles de Gaulle', 'street2': 'PA des Moulinets- Bat A', 'zip': '44800', 'city': 'Saint Herblain', 'country_id': {'name': False, 'code': False}, 'partner_latitude': 0, 'partner_longitude': 0, 'email': 'antoine@teremis.fr', 'phone': '0750552605', 'mobile': False, 'is_company': False, 'color': 0, 'partner_share': False, 'commercial_partner_id': {'name': False, 'phone': False, 'email': False, 'street': False, 'city': False, 'zip': False, 'country_id': {'name': False, 'code': False}, 'is_company': False, 'company_name': False}, 'commercial_company_name': False, 'company_name': False, 'signup_type': False, 'invoice_warn_msg': False, 'supplier_rank': 0, 'customer_rank': 0, 'siret': False, 'sale_warn_msg': False}

        res = super(BaseModel, self)._get_record_values_from_content(name, content_type, content)
        if not res and content:
            completion_id = self.env.ref('file2record_ai.default_record_creation')
            try:
                empty_dict = self._get_default_record_creation_prompt(content)
            except Exception as err:
                _logger.error(err, exc_info=True)
            prompt = ('Create a json dictionary as described in this schema: \n %s to create a %s '
                      'following these data: \n %s') % (empty_dict, self._name, content)
            # res = completion_id.create_completion(prompt=prompt, response_format='json_object')
            # return json.loads(res[0])
            return {'email_normalized': 'antoine@teremis.fr', 'message_bounce': 0, 'name': 'Antoine NEBOUT', 'display_name': 'Antoine NEBOUT', 'parent_id': {'name': False, 'phone': False, 'email': False, 'street': False, 'city': False, 'zip': False, 'country_id': {'name': False, 'code': False}, 'is_company': False, 'company_name': False}, 'ref': False, 'vat': False, 'company_registry': False, 'website': False, 'comment': False, 'active': False, 'employee': False, 'function': False, 'street': '16d Charles de Gaulle', 'street2': 'PA des Moulinets- Bat A', 'zip': '44800', 'city': 'Saint Herblain', 'country_id': {'name': False, 'code': False}, 'partner_latitude': 0, 'partner_longitude': 0, 'email': 'antoine@teremis.fr', 'phone': '0750552605', 'mobile': False, 'is_company': False, 'color': 0, 'partner_share': False, 'commercial_partner_id': {'name': False, 'phone': False, 'email': False, 'street': False, 'city': False, 'zip': False, 'country_id': {'name': False, 'code': False}, 'is_company': False, 'company_name': False}, 'commercial_company_name': False, 'company_name': False, 'signup_type': False, 'invoice_warn_msg': False, 'supplier_rank': 0, 'customer_rank': 0, 'siret': False, 'sale_warn_msg': False}

        return res
