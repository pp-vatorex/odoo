# -*- coding: utf-8 -*-

from odoo import api, fields, models


class WebPImage(models.Model):
	_inherit = 'website'

	enable_webp_cpmpress = fields.Boolean(string = "Enable WebP", default = False)
	webp_image_quality = fields.Integer(string = "WebP Image Quality", default = 95)
