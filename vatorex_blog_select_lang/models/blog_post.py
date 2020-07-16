# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Post(models.Model):
    _inherit = "blog.post"
    language_available_ids = fields.Many2many('res.lang',string='Article languages')

class HTML(models.Model):
    _inherit = "website.page"
    language_available_ids = fields.Many2many('res.lang',string='Website languages')