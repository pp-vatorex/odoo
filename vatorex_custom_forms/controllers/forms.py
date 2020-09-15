# -*- coding: utf-8 -*-
from odoo import http, models, fields, _
from odoo.http import request
from random import random

class WebsiteForm(http.Controller):
    @http.route(['/simple_form'], type='http', auth="user", website=True, methods=['POST','GET'])
    def form_website(self, **post):
        user = request.env.user.partner_id

        values = {}
        if request.httprequest.method == 'POST':
            # no checking on data. Juste update the logged user
            user.write({
                'email': post['email'],
                'company_name': post['company'],
                'website': post['website'],
            })


            #create lead during POST
            crm_lead = request.env['crm.lead']
            values = {
            'name' : 'Opportunity name' + str(random()),
            'partner_id' : user.id
            }

            crm_lead.create(values)

            #send email
            mail = request.env['mail.mail']


            

            template_data = {
                'subject': 'Subject of email ' + str(random()),
                'body_html': 'Message' + str(random()),
                'author_id': user.id,
                'email_from': request.env.company.email or request.env.user.email_formatted,
                'email_to': 'nwi@odoo.com',
            }
            mail.create(template_data)
            values.update({'sended':True})


            #Example
            # if post['subscribe']:
            #     logic

        #return the tample with values
        values.update({'user':user})
        return request.render('vatorex.simple_form',values)
