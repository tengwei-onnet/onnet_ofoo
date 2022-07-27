# -*- coding: utf-8 -*-

{
    'name': 'Onnet Bookshop',
    'version': '1.0.0',
    'category': 'Bookshop',
    'author': 'Justin Wong',
    'sequence': 0,
    'summary': 'Onnet Bookshop Management System',
    'description': """Onnet Bookshop Management System""",
    'depends': ['mail'],
    'data': [
        'security/ir.model.access.csv',  # security file must at first
        'data/sequence_data.xml',
        'wizard/cancel_record_view.xml',
        'views/menu.xml',
        'views/book_view.xml',
        'views/customer_view.xml',
        'views/borrow_view.xml',
        'views/category.xml',
        'views/staff_view.xml',
        'views/attendance_view.xml',
        "reports/onnet_borrow.xml",
        "reports/onnet_book.xml",
    ],
    'demo': [],
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
