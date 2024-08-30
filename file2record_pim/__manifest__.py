# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/algpl.html).
{
    'name': 'File2Record PIM',
    'version': '17.0.0.0.1',
    'author': 'Michel Perrocheau',
    'website': 'https://github.com/myrrkel',
    'summary': "Allows to upload file to create products in PIM",
    'sequence': 0,
    'certificate': '',
    'license': 'LGPL-3',
    'depends': [
        'pim',
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
        'views/product_views.xml',
        'data/ai_question_answer_tag_data.xml',
    ],
    'assets': {},
    'auto_install': False,
    'installable': True,
    'application': False,
}
