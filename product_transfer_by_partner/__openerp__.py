# -*- coding: utf-8 -*-
#################################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Solucións Aloxa S.L. <info@aloxa.eu>
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
#################################################################################
{
    'name': "product_transfer_by_partner",

    'summary': """
        TODO""",

    'description': """
        TODO
    """,

    'author': "Solucions Aloxa S.L.",
    'website': "http://www.eiqui.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'eiqui.com',
    "icon": "/product_transfer_by_partner/static/src/img/vemotv_logo.png",    
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'sale',
    ],

    # always loaded
    'data': [
        "views/inherit_res_partner.xml",
	"views/inherit_stock_view_move_tree.xml",
	"views/inherit_stock_move_search.xml",
    ],
    # only loaded in demonstration mode
    'demo': [        
    ],
}
