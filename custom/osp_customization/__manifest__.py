{
    'name': 'OSP Customization',
    'version': '14.0.1.0.0',
    'author': 'Anonymous',
    'category': 'Hidden',
    'description': """
OSP Customization
=================
""",
    'website': 'https://www.odoo.com/',
    'depends': ['website_crm', 'website_blog', 'intl_phone_field', 'crm'],
    'data': [
        'security/ir.model.access.csv',

        'data/website_crm_data.xml',
        'data/osp_industry_data.xml',

        'views/assets.xml',

        'views/snippets/osp_banner.xml',
        'views/snippets/osp_carousel.xml',
        'views/snippets/osp_features_grid.xml',
        'views/snippets/osp_popup.xml',
        'views/snippets/osp_showcase.xml',
        'views/snippets/osp_tabs.xml',
        'views/snippets/snippets.xml',

        'views/osp_industry_views.xml',
        'views/crm_lead_views.xml',
        'views/webclient_templates.xml',
        'views/website_crm_templates.xml',
        'views/website_form_templates.xml',
        'views/website_templates.xml',
        'views/website_blog_templates.xml',
        'views/website_blog_posts_loop.xml',
    ],
    'installable': True,
    'auto_install': False,
}
