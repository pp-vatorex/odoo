# -*- encoding: utf-8 -*-
{
    'name': 'Vatorex: Custom Blocks',
    'category': 'Hidden',
    'sequence': 7,
    'summary': 'Vatorex: Custom blocks',
    'version': '0.1',
    'description': 'Adds custom Vatorex blocks to the Website builder',
    'depends': [
        'website',
        'website_mail',
        'website_form',
        'website_crm',
    ],
    'images': [
        'static/description/website_theme_screenshot.jpg',
    ],

    'data': [

        # data

        # assets
        'views/frontend/html_assets.xml',

        # layout

        #backend

        # pages
        'views/backend/building_blocks.xml',

        # generic views

    ],

}
