# -*- coding: utf-8 -*-

{
    'name': 'Kingfisher Theme',
    'description': 'Kingfisher Theme',
    'category': 'Theme/Ecommerce',
    'version': '1.1',
    'author': 'Biztech Consultancy',
    'depends': ['website','website_sale','mass_mailing_distribution_list'],
    'data': [
         'views/res_company.xml',          
         'views/partner_view.xml',
        'views/product_view.xml',
        'views/product_config_view.xml',
        'data/data.xml',
        'views/theme.xml', 
        'views/product_template.xml',
        'security/kingfisher_theme.xml',   
        'security/ir.model.access.csv',
    ],
    'live_test_url': 'http://theme-kingfisher.biztechconsultancy.com',
    'images': ['static/description/splash-screen.png'],
    'price': 159.00,
    'currency': 'EUR',
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
