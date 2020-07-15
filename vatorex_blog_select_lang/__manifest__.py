# -*- encoding: utf-8 -*-
{
    'name': 'Vatorex: Blog and blocks select language',
    'category': 'Hidden',
    'sequence': 7,
    'summary': 'Show/hide blog posts / blocks for specific languages',
    'version': '0.1',
    'description': '',
    'depends': [
        'website_blog',
        'website_crm',
    ],
    'images': [
        'static/description/website_theme_screenshot.jpg',
    ],

    'data': [
        # data

        # assets

        # layout

        #backend
        'views/backend/blog_post_form.xml',
        #'views/backend/html_page_form.xml',

        # pages
        'views/frontend/blog_template.xml',

        # generic views
    ],

}
