from openerp import models, fields, api


class res_company(models.Model):
    _inherit = 'res.company'
    
    quotation_name_linked = fields.Boolean( 'Keep Split Quotation Name Pattern?', help='''
    This setting will help you to keep the Split quotation history in the name of the Quotation. 
    For example, enabling this setting and then by splitting the quote SO110,
    new quote will be named as SO110/1 and once again 
    if you split SO110/1, new quote will be named as SO110/1/1
    ''', default=True)
