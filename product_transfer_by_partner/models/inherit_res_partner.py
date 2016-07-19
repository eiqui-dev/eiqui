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

from openerp import models, fields, api

class res_partner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _stock_move_count(self):
        # The current user may not have access rights for stock moves
        try:
            for partner in self:
                partner.total_products = len(partner.stock_move_ids) + \
                len(partner.mapped('child_ids.stock_move_ids'))
        except:
            pass

    
    total_products = fields.Integer(compute='_stock_move_count', 
                                    string='Products', default=0)
    stock_move_ids = fields.One2many('stock.move', 'partner_id', 
                                     'Stock Moves')
