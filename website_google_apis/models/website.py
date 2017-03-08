# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 Solucións Aloxa S.L. <info@aloxa.eu>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, api, fields
import requests
import json


class website(models.Model):
    _inherit = 'website'

    @api.multi
    def is_captcha_valid(self, response):
        for website in self:
            get_res = {
                'secret': website.recaptcha_private_key,
                'response': response
            }
            try:
                response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=get_res)
            except Exception, e:
                raise Exception(('Invalid Data!'), "%s." % e)
            res_con = json.loads(response.content)
            if 'success' in res_con and res_con['success']:
                return True
        return False

    recaptcha_site_key = fields.Char('reCAPTCHA Site Key')
    recaptcha_private_key = fields.Char('reCAPTCHA Private Key')
    google_maps_key = fields.Char('Google Maps Key')
    google_oauth2 = fields.Char('Google OAuth 2.0 Key')
