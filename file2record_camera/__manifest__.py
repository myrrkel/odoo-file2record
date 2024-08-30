# Copyright (C) 2024 - Michel Perrocheau (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/algpl.html).
{
    'name': 'Upload Record Camera',
    'version': '17.0.0.0.1',
    'author': 'Michel Perrocheau',
    'website': 'https://github.com/myrrkel',
    'summary': "Allows to upload Image from camera to any model",
    'sequence': 0,
    'certificate': '',
    'license': 'LGPL-3',
    'depends': [
        'web',
        'file2record',
        'file2record_image',
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
            'file2record_camera/static/src/xml/webcam_upload.xml',
            'file2record_camera/static/src/xml/list_controller.xml',
            'file2record_camera/static/src/js/list_controller.js',
        ],
    },
    'auto_install': False,
    'installable': True,
    'application': False,
}
