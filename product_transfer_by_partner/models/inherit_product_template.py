# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api

class product_template(models.Model):
    _inherit = 'product.template'

    @api.multi
    def _stock_move_count(self):
        res_partner_obj = self.env['res.partner']
        
        res_partner_ids = res_partner_obj.search([])
        for partner in res_partner_ids:
            for product_tmpl in self:
                for stock_move in partner.stock_move_ids:
                    if stock_move.product_tmpl_id == product_tmpl:
                        product_tmpl.total_partners += 1
                        break

    
    total_partners = fields.Integer(compute='_stock_move_count', 
                                    string='Partners', default=0)
    






