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
from openerp import models, fields, api, exceptions


class jsonrpc_keys(models.Model):
    _name='jsonrpc.keys'
    
    @api.v8
    def check_key(self, key, url):
        key_id = self.search([('key', '=', key), ('actived', '=', True)], limit=1)
        if not key_id:
            return None
        
        if len(key_id.urls) > 0:
            clean_url = url.split('?')[0]
            urls = key_id.urls.split('\n')
            if not clean_url in urls:
                return None
        
        return key_id.user_id
    
    
    key = fields.Char(string='JSON-RPC Key', size=128, required=True, unique=True)
    user_id = fields.Many2one('res.users', string='User', required=True)
    actived = fields.Boolean(string='Activated?', default=True)
    urls = fields.Char(string='URLs Affected')
    