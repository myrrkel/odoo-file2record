# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/algpl.html).
{
    'name': 'File2Record AI',
    'version': '16.1.0.0',
    'author': 'Michel Perrocheau',
    'website': 'https://github.com/myrrkel',
    'summary': "Allows to upload file an create record with AI",
    'sequence': 0,
    'certificate': '',
    'license': 'LGPL-3',
    'depends': [
        'file2record',
        'ai_connector',
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
        'data/ai_completion_data.xml',
    ],
    'assets': {

    },
    'auto_install': False,
    'installable': True,
    'application': False,
}
