# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/algpl.html).
{
    'name': 'File2Record Image',
    'version': '16.1.0.0',
    'author': 'Michel Perrocheau',
    'website': 'https://github.com/myrrkel',
    'summary': "Allows to upload Image for any model",
    'sequence': 0,
    'certificate': '',
    'license': 'LGPL-3',
    'depends': [
        'file2record',
    ],
    'external_dependencies': {
        'python': ['pytesseract', 'opencv-python'],
        'bin': ['tesseract'],
    },
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

    ],
    'assets': {

    },
    'auto_install': False,
    'installable': True,
    'application': False,
}
