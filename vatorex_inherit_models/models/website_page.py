# -*- coding: utf-8 -*-
from odoo import api, fields, models


class website_page(models.Model):
    _inherit = "website.page"
    name = fields.Char(string='Description', translate=True)