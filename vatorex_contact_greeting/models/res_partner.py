# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    greeting_msg = fields.Text(compute='_compute_greeting_msg',store=True, translate=True)
    gender = fields.Selection([('female', 'F'), ('male', 'M'), ('unknown', 'Unknown')], required=True, default='unknown')
    type_greeting_msg = fields.Selection([('informal', 'Informal'), ('formal', 'Formal')], required=True, default='formal')
    greeting_text_informal = fields.text('Hello', store=True, translate=True)
    greeting_text_formal_female = fields.text('Dear Mrs', store=True, translate=True)
    greeting_text_formal_male = fields.text('Dear Mr', store=True, translate=True)
    greeting_text_formal_unknown = fields.text('Dear', store=True, translate=True)

    @api.depends('firstname', 'lastname','type_greeting_msg', 'gender')
    def _compute_greeting_msg(self):
        for record in self:
            if record.type_greeting_msg == 'informal':
                record.greeting_msg = record.greeting_text_informal + ' ' + record.firstname
            else if record.type_greeting_msg == 'formal':
                if record.gender == 'female'
                    record.greeting_msg = record.greeting_text_formal_female + ' ' + record.lastname
                else if record.gender == 'male'
                    record.greeting_msg = record.greeting_text_formal_male + ' ' + record.lastname
                else if record.gender == 'unknown'
                    record.greeting_msg = record.greeting_text_formal_unknown + ' ' + record.name