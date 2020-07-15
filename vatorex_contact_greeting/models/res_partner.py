# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    greeting_msg = fields.Text(compute='_compute_greeting_msg',store=True, translate=True)
    gender = fields.Selection([('female', 'F'), ('malea', 'M'), ('unknown', 'Unknown')], required=True, default='unknown')
    type_greeting_msg = fields.Selection([('informal', 'Informal'), ('formal', 'Formal')], required=True, default='formal')

    @api.depends('firstname', 'lastname','type_greeting_msg', 'gender')
    def _compute_greeting_msg(self):
        for record in self:
            if record.type_greeting_msg == 'informal':
                record.greeting_msg = record.type_greeting_msg + " " + record.name + record.gender

            if record.type_greeting_msg == 'formal':
                record.greeting_msg = record.type_greeting_msg + " " + record.name + record.gender
