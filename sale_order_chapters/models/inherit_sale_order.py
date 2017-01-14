# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2017 Solucións Aloxa S.L. <info@aloxa.eu>
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
from openerp import models, fields, api, _

class sale_order(models.Model):
    _inherit = 'sale.order'
    
    revisions = fields.One2many('sale_order_chapters.revision', 'sale_order_id', 'Revisions')
    
    @api.model
    def create(self, vals):
        new_id = super(sale_order, self).create(vals)
        if len(self.revisions) == 0:
            rev = self.env['sale_order_chapters.revision'].create({
                'reason': _('Initial Proposal'),
                'sale_order_id': new_id.id
            })
            self.write({'revisions': (0, 0, rev)})
        return new_id