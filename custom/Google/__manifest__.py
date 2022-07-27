# -*- coding: utf-8 -*-

{
    'name': 'Google',
    'version': '1.0.0',
    'category': 'website',
    'author': 'Elon Mask',
    'sequence': -100,
    'summary': 'Toyota Management System',
    'description': """Toyota Management System""",
    'depends': [],
    'data': [
        'security/ir.model.access.csv', #security file must at first
        'views/menu.xml',
        'views/car_view.xml',
    ],
    'demo': [],
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
