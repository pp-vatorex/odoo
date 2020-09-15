# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    first_name = fields.Char('First Name',required=True,default='First Name')
    last_name = fields.Char('Last Name',required=True,default='Last Name')
    name = fields.Char(compute='_compute_name',store=True,required=False,index=True) #maybe to thing about reverse (means give the possibility to edit the computed field name)
    greeting_msg = fields.Text(compute='_compute_greeting_msg',store=True, translate=True)
    type_greeting_msg = fields.Selection([('informal', 'Informal'), ('formal', 'Formal')], required=True, default='formal')

    _sql_constraints = [
        ('check_name', "CHECK( (type='contact') or (type!='contact') )", 'Contacts require a name'),
    ] # NEED TO CHECKKK ..... 

    @api.depends('first_name','last_name')
    def _compute_name(self):
        for record in self:
            record.name = record.first_name + " " + record.last_name

    @api.depends('first_name','last_name','type_greeting_msg')
    def _compute_greeting_msg(self):
        for record in self:
            if record.type_greeting_msg == 'informal':
                record.greeting_msg = record.type_greeting_msg + " " + record.first_name

            if record.type_greeting_msg == 'formal':
                record.greeting_msg = record.type_greeting_msg + " " + record.last_name
