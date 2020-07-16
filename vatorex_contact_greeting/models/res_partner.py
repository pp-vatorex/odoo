# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    greeting_msg = fields.Text(compute='_compute_greeting_msg',store=True, translate=True)
    gender = fields.Selection([('female', 'Female'), ('male', 'Male'), ('unknown', 'Unknown')], required=True, default='unknown')
    type_greeting_msg = fields.Selection([('informal', 'Informal'), ('formal', 'Formal')], required=True, default='formal')
    greeting_text_informal = 'Hello'
    greeting_text_formal_female = 'Dear Mrs'
    greeting_text_formal_male = 'Dear Mr'
    greeting_text_formal_unknown = 'Dear'

    @api.depends('firstname', 'lastname', 'name', 'type_greeting_msg', 'gender')
    def _compute_greeting_msg(self):
        for record in self:
            if record.type_greeting_msg == 'informal':
                record.greeting_msg = record.greeting_text_informal + ' ' + record.firstname
            elif record.type_greeting_msg == 'formal':
                if record.gender == 'female':
                    record.greeting_msg = record.greeting_text_formal_female + ' ' + record.lastname
                elif record.gender == 'male':
                    record.greeting_msg = record.greeting_text_formal_male + ' ' + record.lastname
                elif record.gender == 'unknown':
                    record.greeting_msg = 'Dear ' + record.name
