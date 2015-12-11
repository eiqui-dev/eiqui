from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.exceptions import except_orm

class quotation_split(models.TransientModel):
    _name = 'quotation.split'
    
    partner_id = fields.Many2one('res.partner', 'Customer', help="Choose customer for new sales order.")
    pricelist_id = fields.Many2one('product.pricelist', 'Pricelist', help="Pricelist for new sales order.")
    
    @api.v7
    def default_get(self, cr, uid, fields, context=None):
        res = super(quotation_split, self).default_get(cr, uid, fields, context=context)  
        order_line_ids = context.get('active_ids',False)
        if order_line_ids:
            order_lines = self.pool.get('sale.order.line').browse(cr, uid, order_line_ids, context=context)
            if order_lines:
                res['partner_id'] = order_lines[0].order_id.partner_id.id
        return res
    
    
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        pricelist_id = False
        if self.partner_id:
            pricelist = self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False
            pricelist_id = pricelist
        self.pricelist_id = pricelist_id
    
    @api.one
    def get_new_order_name(self,sale_order):
        new_name = sale_order.name
        new_level = sale_order.splitting_counter + 1
        new_name = new_name +  '/' + str(new_level)
        return new_name, sale_order.splitting_counter + 1
    
    @api.one
    def set_new_price(self, new_order,order_line):
        res = order_line.product_id_change(new_order.pricelist_id.id, order_line.product_id.id, qty=order_line.product_uom_qty,
            uom=False, qty_uos=order_line.product_uos_qty, uos=False, name='', partner_id=new_order.partner_id.id,
            lang=False, update_tax=True, date_order=new_order.date_order, packaging=False, fiscal_position=False, flag=False)
        return res['value']
    
    @api.one
    def confirm_quotation_split(self):
        order_line_ids = self._context.get('active_ids',False)
        if not order_line_ids:
            raise except_orm(('Unable to proceed'),('Order does not have enough products to split!!!'))

        sale_order_line_obj = self.env['sale.order.line']
        order_id = sale_order_line_obj.search([('id','=',order_line_ids[0])]).order_id

        new_name, splitting_counter = self.get_new_order_name(order_id)[0]
            
        new_obj = order_id.copy(default = {'order_line' : None,'partner_id' : self.partner_id and self.partner_id.id or order_id.partner_id.id, 
                                           'pricelist_id' : self.pricelist_id and self.pricelist_id.id or order_id.pricelist_id.id,
                                           'splitting_counter' : 0,'split_from' : ''})
        
        order_id.write({'splitting_counter' : splitting_counter})
        new_obj.write({'split_from' : order_id.name})
        
        company = self.env['res.users'].browse(self._uid).company_id
        if company and company.quotation_name_linked: 
            new_obj.name = new_name
        
        if not order_id.partner_id.id == new_obj.partner_id.id:
            vals = new_obj.onchange_partner_id(new_obj.partner_id.id)
            vals['value']['pricelist_id'] = new_obj.pricelist_id.id
            new_obj.write(vals['value'])
        
        if self.pricelist_id:
            ## update price of existing product
            for dx in order_line_ids:
                line = sale_order_line_obj.browse(dx)
                new_line_data = self.set_new_price(new_obj,line)
                new_line = line.copy(default = {'order_id' : new_obj.id})
                new_line.write(new_line_data and new_line_data[0] or {})
                line.unlink()
        else:
            for dx in order_line_ids:
                line = sale_order_line_obj.browse(dx)
                line.copy(default = {'order_id' : new_obj.id})
                line.unlink()
            
        return new_obj.id
    
    @api.multi
    def confirm_quotation_split_view(self):
        new_order_id = self.confirm_quotation_split()
        if not new_order_id :
            return except_orm(('Unable to proceed'),('There is some problem while creating new quotation, please contact your administrator!!!'))
        
        model_obj = self.env['ir.model.data']
        data_id = model_obj._get_id('sale', 'view_order_form')
        view_id = model_obj.browse(data_id).res_id
        res = self._context.copy() or {}
        res.update({'active_id': new_order_id[0]})
        return {
            'type': 'ir.actions.act_window',
            'name': _('Sale Order'),
            'res_model': 'sale.order',
            'res_id': new_order_id[0],
            'view_type' : 'form',
            'view_mode' : 'form',
            'view_id' : view_id,
            'target' : 'current',
            'nodestroy' : True,
            'context'  : res,
              }
 

    