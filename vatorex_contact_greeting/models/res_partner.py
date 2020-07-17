# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # example_to_translate_with_pot_and_po = _("translate me")

    # English (default greeting messages)
    greeting_text_informal = "Hello"
    greeting_text_formal_female = 'Dear Mrs'
    greeting_text_formal_male = 'Dear Mr'
    greeting_text_formal_unknown = 'Dear'

    # German
    if record.lang == 'de_DE':
        greeting_text_informal = "Hallo"
        greeting_text_formal_female = 'Sehr geehrte Frau'
        greeting_text_formal_male = 'Sehr geehrter Herr'
        greeting_text_formal_unknown = 'Sehr geehrte/r'

    greeting_msg = fields.Text(compute='_compute_greeting_msg',store=True, translate=True)
    gender = fields.Selection([('female', 'Female'), ('male', 'Male'), ('unknown', 'Unknown')], required=True, default='unknown')
    type_greeting_msg = fields.Selection([('informal', 'Informal'), ('formal', 'Formal')], required=True, default='formal')

    @api.depends('firstname', 'lastname', 'name', 'type_greeting_msg', 'gender')
    def _compute_greeting_msg(self):
        for record in self:
            if record.type_greeting_msg == 'informal':
                record.greeting_msg = greeting_text_informal + ' ' + record.firstname
            elif record.type_greeting_msg == 'formal':
                if record.gender == 'female':
                    record.greeting_msg = greeting_text_formal_female + ' ' + record.lastname
                elif record.gender == 'male':
                    record.greeting_msg = greeting_text_formal_male + ' ' + record.lastname
                elif record.gender == 'unknown':
                    record.greeting_msg = greeting_text_formal_male + ' ' + record.name
