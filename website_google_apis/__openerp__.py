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
    'name': "Website Google API's",
    'version': '1.0',
    'category': 'Website',
    'depends': ['website'],
    'author': 'Solucións Aloxa S.L.',
    'license': 'AGPL-3',
    'website': 'https://www.eiqui.com',
    'description': """
Odoo Website Google API's
================================
This modules allows you to integrate Google API's to your website pages.
You can configure your Google API's app keys
in "Settings" -> "Website Settings"
""",
    'data': [
        'views/website_view.xml',
        'views/res_config.xml',
    ],
    'installable': True,
    'auto_install': False
}
