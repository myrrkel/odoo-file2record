# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, _, api
import logging
import base64
import requests
import re


def is_valid_url(url):
    pattern = r'^(?:http|ftp)s?://(?:\S+(?::\S*)?@)?(?:(?:[a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9])\.)+[a-zA-Z]{2,63}(?::\d{2,5})?(?:/\S*)?$'
    return bool(re.match(pattern, url))


_logger = logging.getLogger(__name__)


class BaseModel(models.AbstractModel):
    _inherit = 'base'

    def create_record_from_text(self, text):
        res = []
        if is_valid_url(text):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
            text = requests.get(text, headers=headers).text
            values = self._get_record_values('', 'html', text)
        else:
            values = self._get_record_values('', 'text', text)
        if values:
            rec_id = self._create_record_from_dict(values)
            if rec_id:
                res.append(rec_id.id)
        return self.get_record_creation_result_action(res)
