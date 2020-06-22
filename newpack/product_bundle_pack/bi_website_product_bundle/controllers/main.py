# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
##############################################################################

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
          
class ProductBundle(WebsiteSale):

    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>'
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):

        res=super(ProductBundle, self).shop(page, category, search, **post)

        product_pack =request.env['product.template'].sudo().search([('is_pack','=',True)])
        
        for pack_record in product_pack:
            pack_record.sudo().website_style_ids = [[6,0,[1]]]

        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
