# -*- coding: utf-8 -*-
from odoo import http
import werkzeug
from odoo.http import request
from odoo.addons.website_blog.controllers.main import WebsiteBlog
from odoo.addons.website.controllers.main import QueryURL

class WebsiteBlog(WebsiteBlog):

    # @http.route([
    #     '/blog',
    #     '/blog/page/<int:page>',
    #     '/blog/tag/<string:tag>/page/<int:page>',
    #     '''/blog/<model("blog.blog", "[('website_id', 'in', (False, current_website_id))]"):blog>''',
    #     '''/blog/<model("blog.blog"):blog>/page/<int:page>''',
    #     '''/blog/<model("blog.blog"):blog>/tag/<string:tag>''',
    #     '''/blog/<model("blog.blog"):blog>/tag/<string:tag>/page/<int:page>''',
    # ], type='http', auth="public", website=True)

    # def blog(self, blog=None, tag=None, page=1, **opt):
    #     result = super(WebsiteBlog,self).blog(blog, tag, page, **opt)
    #     posts = result.qcontext['posts']
    #     if posts:
    #         current_lang = request.env['res.lang'].search([('code','=',request.context['lang'])])
    #         s = posts.filtered(lambda r: current_lang in r.language_available_ids )
    #     result.qcontext.update({'posts':s})
    #     return result
