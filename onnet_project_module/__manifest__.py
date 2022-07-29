# -*- coding: utf-8 -*-

{
    'name': 'Onnet Project',
    'version': '1.0.0',
    'category': 'project',
    'author': 'Justin Wong',
    'description': """Onnet Project Customize""",
    'depends': ['project', 'base', 'helpdesk'],
    'data': [
        'security/ir.model.access.csv',  # security file must at first
        'data/sequence_data.xml',
        'views/project_task_view.xml',
        'views/onnet_res_users_view.xml',
    ],
    'demo': [],
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
