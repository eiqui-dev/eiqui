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

from openerp.osv import fields,osv

class res_partner(osv.osv):
    _inherit = 'res.partner'

    def _stock_move_count(self, cr, uid, ids, field_name, arg, context=None):
        res = dict(map(lambda x: (x,0), ids))
        # The current user may not have access rights for stock moves
        try:
            for partner in self.browse(cr, uid, ids, context):
                res[partner.id] = len(partner.stock_move_ids) + len(partner.mapped('child_ids.stock_move_ids'))
        except:
            pass
        return res

    _columns = {
        'total_products': fields.function(_stock_move_count, string='Products', type='integer'),
        'stock_move_ids': fields.one2many('stock.move','partner_id','Stock Moves')
    }






