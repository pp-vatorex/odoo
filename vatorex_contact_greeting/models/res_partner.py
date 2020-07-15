# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    greeting_msg = fields.Text(compute='_compute_greeting_msg',store=True, translate=True)
    type_greeting_msg = fields.Selection([('informal', 'Informal'), ('formal', 'Formal')], required=True, default='formal')

    @api.depends('name','type_greeting_msg')
    def _compute_greeting_msg(self):
        for record in self:
            if record.type_greeting_msg == 'informal':
                record.greeting_msg = record.type_greeting_msg + " " + record.name

            if record.type_greeting_msg == 'formal':
                record.greeting_msg = record.type_greeting_msg + " " + record.name
