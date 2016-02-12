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
    'name': "dochsync",

    'summary': """
        Sincronización de almacén de Documentos con nombres humanos""",

    'description': """
        Mapeo del almacén de Documentos de Odoo para crear una estructura de directorios paralela
        con nombres humanos, de modo que la estructura de Documentos aparezca anidada de modo cohente
        y accesible desde otros sistemas, por ejemplo Owncloud.
        Tambien permite la sincronizacion inversa, esto es, los archivos subidos a traves de plataformas
        de gestion de archivos como Owncloud se sincronizan con el modulo de gestion documental de Odoo
    """,

    'author': "Javier Fernández Peón (eiqui).",
    'website': "http://www.eiqui.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Filestore',
    "icon": "/aloxa_docs_ocsync/static/src/img/icon.png",    
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'document', 'subscription'],

    # always loaded
    'data': [
        'view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [        
    ],
    "installable": True,
}