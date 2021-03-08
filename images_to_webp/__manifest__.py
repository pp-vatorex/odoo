# -*- coding: utf-8 -*-
{
	"name"                 : "WebP Image Optimizer",
	"summary"              : "WebP Image Optimizer",
	"description"          : """
		Install dependencies:
		`pip3 install webp`
		`pip3 install cssselect`
	""",
	'author'               : "eSwap",
	"category"             : "Website",
	"version"              : "13.0.1.2",
	"sequence"             : 1,
	'license'              : 'OPL-1',
	"depends"              : ['website'],
	"data"                 : [
		'views/assets.xml',
		'views/views.xml',
	],
	'images'               : [
			'static/description/banner.png',
			'static/description/banner.jpg',
			],
	"external_dependencies": {
		"python": [
			"webp",
			"cssselect",
			"lxml"
		],
	},
	"application"          : True,
	'installable'          : True,
	'auto_install'         : True,
	"support"              : "odoo@eswap.ch",
	"price"                : 50,
	"currency"             : "EUR",
}
