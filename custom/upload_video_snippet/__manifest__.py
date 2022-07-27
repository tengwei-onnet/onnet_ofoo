# -*- coding: utf-8 -*-
{
    'name': "upload video in website builder",

    'summary': """
        allow users to upload video in website builder""",

    'description': """
        change the behavior of uploading video, when user build website, they can select video from their computer and upload to server
    """,
    'author': "harry",
    'website': "https://www.zdctech.top/",
    'category': 'Website',
    'version': '1.0.1',
    'depends': ['base', 'website'],
    'images': [
        'static/description/screen.png'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/snippets/s_video.xml',
        'views/snippets/snippets.xml',
        'views/video_upload_views.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'license': 'LGPL-3',
    'price': 1.0,
    'currency': 'USD',
    'support': '2426548297@qq.com'
}
