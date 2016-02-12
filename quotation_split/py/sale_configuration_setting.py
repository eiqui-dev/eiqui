from openerp import models, fields, api


class sale_config_settings(models.TransientModel):
    _inherit = 'sale.config.settings'
    
    group_allow_splitting = fields.Boolean('Permitir division de Presupuestos', 
                        implied_group='sale.group_sale_split',                                     
                        help = 'You can allow user to choose new customer and price lists for the quotation which will going to be created.')