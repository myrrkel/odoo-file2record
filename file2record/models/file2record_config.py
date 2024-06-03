# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields, api, _
from odoo.tools.safe_eval import safe_eval
from odoo.addons.base.models.ir_model import SAFE_EVAL_BASE
import logging

_logger = logging.getLogger(__name__)


class UploadFileConfig(models.Model):
    _name = 'file2record.config'
    _description = 'File2Record Config'

    def _get_record_creation_method_list(self):
        return [('method', _('Model Method')),
                ('code', _('Code')),]

    def _get_data_type_list(self):
        return [('text', _('Text')),
                ('pdf', _('PDF')),
                ('doc', _('Word/OpenOffice')),
                ('html', _('HTML')),
                ('xml', _('XML')),
                ('bin', _('Binary')),
                ]

    def _get_post_process_list(self):
        return [('code', _('Python Code')),
                ('method', _('Model Method')),
                ]

    name = fields.Char()
    description = fields.Text()
    model_id = fields.Many2one('ir.model', string='Model', ondelete='cascade')
    data_type = fields.Selection(selection=_get_data_type_list)
    model = fields.Char(related='model_id.model', string='Model Name', readonly=True, store=True)
    record_creation_method = fields.Selection(selection=_get_record_creation_method_list)
    code = fields.Text()
    post_process = fields.Selection(selection='_get_post_process_list')
    post_process_code = fields.Text()
    model_record_creation_method = fields.Char()
    model_post_process_method = fields.Char()
    show_upload_file_button = fields.Boolean(default=True)

    @api.model
    def is_file_to_record_button_visible(self, model):
        if self.search([('model', '=', model), ('show_upload_file_button', '=', True)]):
            return True

    def eval_record_creation_code(self, content):
        res = False
        local_dict = {'self': self, 'res': res, 'content': content}
        safe_eval(self.code, SAFE_EVAL_BASE, local_dict, mode='exec', nocopy=True)
        return local_dict['res']

    def eval_post_process_code(self, values):
        res = False
        local_dict = {'self': self, 'res': res, 'values': values}
        safe_eval(self.post_process_code, SAFE_EVAL_BASE, local_dict, mode='exec', nocopy=True)
        return local_dict['res']
