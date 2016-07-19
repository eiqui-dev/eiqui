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
{
    'name': "product_transfer_by_partner",

    'summary': """
        Smart Button to view products solds and return from partner form""",

    'description': """
        This module create a smart button in the partner form to show the stock moves links with the partner. 
	    It also creates a filter for the lot, and displays the partner in the list view of the movements.
    """,

    'author': """Alexandre Díaz Cuadrado (eiqui.com -aloxa.eu-)
		Darío Lodeiros Vázquez (eiqui.com -aloxa.eu-)
		""",
    'website': "http://www.eiqui.com",

    'category': 'Accounting &amp; Finance',
    "icon": "/product_transfer_by_partner/static/src/img/icon.png",    
    'version': '0.1',

    'depends': [
        'base',
        'sale',
        'stock',
    ],

    'data': [
        "views/inherit_res_partner.xml",
	    "views/inherit_stock_view_move_tree.xml",
        "views/inherit_stock_move_search.xml",
        "views/inherit_product_product.xml",
        "views/inherit_product_template.xml",
    ],

    'demo': [],
}
