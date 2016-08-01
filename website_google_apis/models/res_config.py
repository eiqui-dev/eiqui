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

from openerp.osv import fields, osv


class website_config_settings(osv.osv_memory):
    _inherit = 'website.config.settings'
    
    _columns = {
        'recaptcha_site_key': fields.related(
            'website_id', 'recaptcha_site_key', type="char",
            string='reCAPTCHA Site Key'),
        'recaptcha_private_key': fields.related(
            'website_id', 'recaptcha_private_key', type="char",
            string='reCAPTCHA Private Key'),
        'google_maps_key': fields.related(
            'website_id', 'google_maps_key', type="char",
            string='Google Maps Key'),
        'google_oauth2': fields.related(
            'website_id', 'google_oauth2', type="char",
            string='Google OAuth 2.0 Key'),
    }
