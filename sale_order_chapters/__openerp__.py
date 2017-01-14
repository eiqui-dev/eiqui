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

# TODO: Meter el capitulo de 

{
    'name': 'Sale Order Chapters',
    'version': '0.1',
    'author': "Alexandre Díaz (Aloxa Solucións S.L.) <alex@aloxa.eu>",
    'website': 'https://www.eiqui.com',
    'category': '',
    'summary': "Group Invoice Lines by Chapter",
    'description': "",
    'depends': ['sale','report', 'product', 'qweb_usertime'],
    'data': [
        'views/reports/external_layout_footer.xml',
        'views/reports/external_layout_header.xml',
        'views/reports/external_layout.xml',
        'views/reports/report_sale_order_document.xml',
        'views/reports/report_sale_order.xml',
        'views/reports/report_style.xml',
        'data/paper_formats.xml',
        'views/inherit_sale_order.xml',
        'views/inherit_product_template.xml',
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'AGPL-3',
}
