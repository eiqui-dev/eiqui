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
    'name': 'Report Picking Translate',
    'version': '0.1',
    'author': "Darío Lodeiros Vázquez (Aloxa Solucións S.L.) <dario@aloxa.eu>",
    'website': 'https://www.aloxa.eu',
    'category': '',
    'summary': "Make translate report picking",
    'description': "",
    'depends': [
        'stock',
    ],
    'data': [
        'views/report_picking_translate.xml',
	'data/report_picking.xml',
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'AGPL-3',
}
