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
            res = completion_id.create_completion(prompt=prompt)
            return json.loads(res[0])

        res = super(BaseModel, self)._get_record_values_from_content(name, content_type, content)
        if not res and content:
            completion_id = self.env.ref('file2record_ai.default_record_creation')
            try:
                prompt = self._get_default_record_creation_prompt(content)
                res = completion_id.create_completion(prompt=prompt, response_format='json_object')
                if isinstance(res[0], str):
                    return json.loads(res[0])
                else:
                    return json.loads(res[0].answer)
            except Exception as err:
                _logger.error(err, exc_info=True)
        return res

    def _get_values_from_attachment_id(self, attachment_id):
        context = {'model': 'ir.attachment', 'res_id': attachment_id}
        return super(BaseModel, self.with_context(completion=context))._get_values_from_attachment_id(attachment_id)
