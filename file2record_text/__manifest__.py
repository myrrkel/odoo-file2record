# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/algpl.html).
{
    'name': 'File2Record Text',
    'version': '17.0.0.0.1',
    'author': 'Michel Perrocheau',
    'website': 'https://github.com/myrrkel',
    'summary': "Allows to upload text to any model",
    'sequence': 0,
    'certificate': '',
    'license': 'LGPL-3',
    'depends': [
        'web',
        'file2record',
    ],
    'category': 'EDI',
    'complexity': 'easy',
    'qweb': [
    ],
    'demo': [
    ],
    'images': [
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/file2record_config_views.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'file2record_text/static/src/xml/text_upload.xml',
            'file2record_text/static/src/xml/list_controller.xml',
            'file2record_text/static/src/js/list_controller.js',
        ],
    },
    'auto_install': False,
    'installable': True,
    'application': False,
}
