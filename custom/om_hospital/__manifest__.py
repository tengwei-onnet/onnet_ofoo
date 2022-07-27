# -*- coding: utf-8 -*-

{
    'name': 'Hospital Management Test',
    'version': '1.0.0',
    'category': 'Hospital',
    'author': 'Odoo Mates',
    'sequence': -100,
    'summary': 'Hospital Management System',
    'description': """Hospital Management System""",
    'depends': [],
    'data': [
        'security/ir.model.access.csv', #security file must at first
        'views/menu.xml',
        'views/patient_view.xml',
        'views/appointment_view.xml',
    ],
    'demo': [],
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
