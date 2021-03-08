# -*- coding: utf-8 -*-
import odoo
from odoo import http, tools, _
from odoo.tools import image_process
from odoo.http import request
from odoo.addons.web.controllers.main import Binary
from odoo.addons.web_editor.controllers.main import Web_Editor
from odoo.exceptions import UserError
import base64, io, webp
from PIL import Image
from ..models.ir_ui_view import check_webp_support


class Binary(Binary):
	def _content_image(self, xmlid = None, model = 'ir.attachment', id = None, field = 'datas',
	                   filename_field = 'name', unique = None, filename = None, mimetype = None,
	                   download = None, width = 0, height = 0, crop = False, quality = 0, access_token = None,
	                   placeholder = 'placeholder.png', **kwargs):
		webp_support = check_webp_support(request)
		convert_back_to_png = False
		w = width
		h = height

		if model and model == 'ir.attachment' and id:
			attachment = request.env[model].sudo().search([('id', '=', id)])

			if attachment and attachment.mimetype == "image/webp":
				quality = 0
				width = 0
				height = 0
				crop = False

				if not webp_support:
					convert_back_to_png = True

		response = super(Binary, self)._content_image(xmlid = xmlid, model = model, id = id, field = field,
		                                              filename_field = filename_field, unique = unique,
		                                              filename = filename,
		                                              mimetype = mimetype,
		                                              download = download, width = width, height = height, crop = crop,
		                                              quality = quality, access_token = access_token)

		if convert_back_to_png and response.data:
			img_data = response.data
			webp_data = webp.WebPData.from_buffer(img_data)
			arr = webp_data.decode()
			source_image = Image.fromarray(arr, 'RGBA')

			if w or h:
				source_image.thumbnail((w, h))

			convert_to_png = io.BytesIO()
			source_image.save(convert_to_png, 'PNG')
			response.data = convert_to_png.getvalue()

		return response


class WebP(http.Controller):
	@http.route([
			'/webp/image',
			'/webp/image/<string:xmlid>',
			'/webp/image/<string:xmlid>/<string:filename>',
			'/webp/image/<string:xmlid>/<int:width>x<int:height>',
			'/webp/image/<string:xmlid>/<int:width>x<int:height>/<string:filename>',
			'/webp/image/<string:model>/<int:id>/<string:field>',
			'/webp/image/<string:model>/<int:id>/<string:field>/<string:filename>',
			'/webp/image/<string:model>/<int:id>/<string:field>/<int:width>x<int:height>',
			'/webp/image/<string:model>/<int:id>/<string:field>/<int:width>x<int:height>/<string:filename>',
			'/webp/image/<int:id>',
			'/webp/image/<int:id>/<string:filename>',
			'/webp/image/<int:id>/<int:width>x<int:height>',
			'/webp/image/<int:id>/<int:width>x<int:height>/<string:filename>',
			'/webp/image/<int:id>-<string:unique>',
			'/webp/image/<int:id>-<string:unique>/<string:filename>',
			'/webp/image/<int:id>-<string:unique>/<int:width>x<int:height>',
			'/webp/image/<int:id>-<string:unique>/<int:width>x<int:height>/<string:filename>'
			], type = 'http', auth = "public")
	def content_image(self, xmlid = None, model = 'ir.attachment', id = None, field = 'datas',
	                  filename_field = 'name', unique = None, filename = None, mimetype = None,
	                  download = None, width = 0, height = 0, crop = False, access_token = None,
	                  **kwargs):
		return self._content_image(xmlid = xmlid, model = model, id = id, field = field,
		                           filename_field = filename_field, unique = unique, filename = filename,
		                           mimetype = mimetype,
		                           download = download, width = width, height = height, crop = crop,
		                           quality = int(kwargs.get('quality', 0)), access_token = access_token)

	def _content_image(self, xmlid = None, model = 'ir.attachment', id = None, field = 'datas',
	                   filename_field = 'name', unique = None, filename = None, mimetype = None,
	                   download = None, width = 0, height = 0, crop = False, quality = 0, access_token = None,
	                   placeholder = 'placeholder.png', **kwargs):
		webp_support = check_webp_support(request)
		is_webp = False

		if model and model == 'ir.attachment' and id:
			attachment = request.env[model].sudo().search([('id', '=', id)])
		else:
			attachment = request.env['ir.attachment'].sudo().search([('res_model', '=', model),
			                                                         ('res_id', '=', id),
			                                                         ('res_field', '=', field)], limit = 1)

		if attachment and attachment.mimetype == "image/webp":
			is_webp = True

		status, headers, image_base64 = request.env['ir.http'].binary_content(
				xmlid = xmlid, model = model, id = id, field = field, unique = unique, filename = filename,
				filename_field = filename_field, download = download, mimetype = mimetype,
				default_mimetype = 'image/png', access_token = access_token)

		if status in [301, 304] or (status != 200 and download):
			return request.env['ir.http']._response_by_status(status, headers, image_base64)
		if not image_base64:
			status = 200
			image_base64 = base64.b64encode(Binary().placeholder(image = placeholder))
			if not (width or height):
				width, height = odoo.tools.image_guess_size_from_field_name(field)

		if not is_webp:
			image_base64 = image_process(image_base64, size = (int(width), int(height)), crop = crop,
			                             quality = quality)
		else:
			if webp_support:
				width = width or height or 0
				height = height or width or 0

				webp_data = webp.WebPData.from_buffer(base64.b64decode(image_base64))
				arr = webp_data.decode()
				source_image = Image.fromarray(arr, 'RGBA')

				if width or height:
					source_image.thumbnail((width, height))

				pic = webp.WebPPicture.from_pil(source_image)
				config = webp.WebPConfig.new(preset = webp.WebPPreset.PHOTO, quality = quality or int(request.session.get('webp_image_quality', 95)) or 95)
				image_base64 = base64.b64encode(pic.encode(config).buffer())

		img_data = base64.b64decode(image_base64)
		headers = http.set_safe_image_headers(headers, img_data)

		if headers and dict(headers).get('Content-Type', '') != 'image/svg+xml':
			width = width or height or 0
			height = height or width or 0

			if webp_support:
				quality = quality or int(request.session.get('webp_image_quality', 95)) or 95

				if not is_webp:
					source_image = Image.open(io.BytesIO(img_data)).convert("RGBA")
					pic = webp.WebPPicture.from_pil(source_image)
					config = webp.WebPConfig.new(preset = webp.WebPPreset.PHOTO, quality = quality)
					img_data = pic.encode(config).buffer()
			else:
				if is_webp:
					webp_data = webp.WebPData.from_buffer(img_data)
					arr = webp_data.decode()
					source_image = Image.fromarray(arr, 'RGBA')

					if width or height:
						source_image.thumbnail((width, height))

					convert_to_png = io.BytesIO()
					source_image.save(convert_to_png, 'PNG')
					img_data = convert_to_png.getvalue()

			for key, item in enumerate(headers):
				if item[0] == 'Content-Type':
					headers[key] = ('Content-Type', webp_support and 'image/webp' or 'image/png')
					break

		response = request.make_response(img_data, headers)
		response.status_code = status
		return response


class Web_Editor(Web_Editor):
	@http.route('/web_editor/attachment/add_data', type = 'json', auth = 'user', methods = ['POST'], website = True)
	def add_data(self, name, data, quality = 0, width = 0, height = 0, res_id = False, res_model = 'ir.ui.view',
	             filters = False, **kwargs):
		website = request.website
		webp_config = website and website.enable_webp_cpmpress or False

		if webp_config:
			try:
				data = base64.b64decode(data)
				source_image = Image.open(io.BytesIO(data)).convert("RGBA")
				pic = webp.WebPPicture.from_pil(source_image)
				config = webp.WebPConfig.new(preset = webp.WebPPreset.PHOTO,
				                             quality = quality or website.webp_image_quality or 95)
				data = pic.encode(config).buffer()
				data = base64.b64encode(data)
			except UserError:
				pass  # not an image

			attachment = self._attachment_create(name = name, data = data, res_id = res_id, res_model = res_model,
			                                     filters = filters)
			result = attachment._get_media_info()

			name = name.split('.')[0]
			name += ".webp"
			attachment.name = name
			attachment.mimetype = "image/webp"

			return result
		else:
			return super(Web_Editor, self).add_data(name = name, data = data, quality = quality, width = width,
			                                        height = height,
			                                        res_id = res_id, res_model = res_model,
			                                        filters = filters, **kwargs)

	@http.route('/web_editor/attachment/<model("ir.attachment"):attachment>/update', type = 'json', auth = 'user',
	            methods = ['POST'], website = True)
	def attachment_update(self, attachment, name = None, width = 0, height = 0, quality = 0, copy = False, **kwargs):
		if attachment.type == 'url':
			raise UserError(_("You cannot change the quality, the width or the name of an URL attachment."))

		website = request.website
		webp_config = website and website.enable_webp_cpmpress or False

		if webp_config and attachment.mimetype == "image/webp":
			if copy:
				attachment = attachment.copy()
			data = {}
			if name:
				data['name'] = name
			try:
				data_image = base64.b64decode(attachment.datas)
				webp_data = webp.WebPData.from_buffer(data_image)
				arr = webp_data.decode()
				source_image = Image.fromarray(arr, 'RGBA')

				width = width or height or 0
				height = height or width or 0

				if width or height:
					source_image.thumbnail((width, height))

				pic = webp.WebPPicture.from_pil(source_image)
				config = webp.WebPConfig.new(preset = webp.WebPPreset.PHOTO,
				                             quality = quality or website.webp_image_quality or 95)
				data_image = pic.encode(config).buffer()
				data_image = base64.b64encode(data_image)

				data['datas'] = data_image
				data['mimetype'] = "image/webp"
				data['index_content'] = 'image'
			except UserError:
				pass  # not an image
			attachment.write(data)
			return attachment._get_media_info()
		else:
			return super(Web_Editor, self).attachment_update(attachment = attachment, name = name, width = width,
			                                                 height = height, quality = quality, copy = copy, **kwargs)
