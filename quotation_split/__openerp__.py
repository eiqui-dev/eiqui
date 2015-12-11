{
    'name': 'Sales Quotation Split',
    'version': '1.0.0',
    'category': "Sales",
    'summary': 'Divide large quotation into sub quotations',
    'description': """
        This module is used to split main quotation into sub quotations""",
    'author': 'Emipro Technologies Pvt. Ltd.',
    'website': 'http://emiprotechnologies.com',
    'depends': ['sale'],
    'data': [ 
                'security/ir.model.access.csv',
                'security/sale_security_group.xml',
                'view/view_order_form_ept.xml',
                'view/configuration_setting.xml',
                'view/res_company_view.xml',
                'wizard/create_quotation_wizard.xml',
                'wizard/view_split_quotation_ept.xml',
              ],
    'installable': True,
    'auto_install': False,
    'images': ['static/description/main_screen.png'],
    'application' : True,
    'price': 10.00,
    'currency': 'EUR',
}
