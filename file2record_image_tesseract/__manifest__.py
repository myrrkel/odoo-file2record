# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/algpl.html).
{
    'name': 'File2Record Image Tesseract',
    'version': '19.0.1.0.0',
    'author': 'Michel Perrocheau',
    'website': 'https://github.com/myrrkel',
    'summary': "Add Tesseract OCR support for image processing",
    'sequence': 0,
    'certificate': '',
    'license': 'LGPL-3',
    'depends': [
        'file2record_image',
    ],
    'external_dependencies': {
        'python': ['pytesseract'],
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
        'views/file2record_config_views.xml',
    ],
    'assets': {

    },
    'auto_install': False,
    'installable': True,
    'application': False,
}
