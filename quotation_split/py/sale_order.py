from openerp import models, fields, api, _
from openerp.exceptions import except_orm

class sale_order(models.Model):
    _inherit = "sale.order"
    
#     @api.multi
#     def _splitted_form(self):
#         for order in self:
#             s_names = order.name.split('/')
#             if len(s_names) > 1:
#                 name = s_names[0]
#                 for x in range(1,len(s_names) - 1):
#                     name = name + '/' + s_names[x] 
#                 order.split_from = name
                
    splitting_counter = fields.Integer('Splitted Quotation Counter')
    split_from = fields.Char('Splitted From',size=64)
    
    @api.v7
    def copy_data(self, cr, uid, ids ,default=None, context={}):
        if default is None:
            default = {}
        default.update({'splitting_counter' : 0, 'split_from' : ''})
        return super(sale_order, self).copy_data(cr, uid, ids ,default=default, context=context)
    
    @api.multi
    def action_quotation_split(self):
        res = self._context.copy()
        if not res:
            res = {}
        res.update({
                    'default_order_id':  self.id,
                    })
        
        count =0
        for line in self.order_line:
            count = count + 1
            if count > 1:
                break
        
        if count <= 1:
            raise except_orm(('Incluir productos'),('Necesitamos al menos dos productos para poder dividir !!!'))
        
        if not self.partner_id:
            raise except_orm(('Establecer Cliente'),('Necesitamos un cliente para poder continuar !!!'))
        
        view = self.env.ref('quotation_split.view_quotation_split_ept')
         
        return {
            'type': 'ir.actions.act_window',
            'name': _('Sales Order'),
            'res_model': 'sale.order.line',
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'tree',
            'view_id': view.id,
            'views': [(view.id, 'tree')],
            'target': 'current',
            'nodestroy': True,
            'context' : res,
            'domain' : [('order_id','=',self.id)],
            }
