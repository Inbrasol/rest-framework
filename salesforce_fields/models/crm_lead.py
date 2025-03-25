
from odoo import _, api, fields, models

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    sf_id = fields.Char(string='Salesforce ID', index=True, unique=True)
    sf_integration_status = fields.Selection([
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed')
    ], string='Integration Status', default='pending', help="Status of the Salesforce integration")
    sf_integration_datetime = fields.Datetime(string='Integration Datetime')
    sf_integration_error = fields.Text(string='Integration Error')
    sf_owner_id = fields.many2one('res.partner', string='Salesforce Owner ID', index=True)

class CrmLeadProduct(models.Model):
    
    _inherit = 'crm.lead.product'
    
    sf_id = fields.Char(string='Salesforce ID', index=True, unique=True)
    sf_integration_status = fields.Selection([
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed')
    ], string='Integration Status', default='pending', help="Status of the Salesforce integration")
    sf_integration_datetime = fields.Datetime(string='Integration Datetime')
    sf_integration_error = fields.Text(string='Integration Error')
    sf_pricebook_entry_id = fields.Char(string="Salesforce Price Book Entry ID", index=True)
    sf_pricebook_id = fields.Char(string="Salesforce Price Book ID", index=True)

    #ORM VALUES
    @api.model
    def create(self,values):
        if values.get('product_id') in [False, None, '']:
            template_product_create = self.build_product(values)
            template_product = self.env['product.product'].create(template_product_create)
            values['product_id'] = template_product.id
        return super(CrmLeadProduct, self).create(values)


    # VALIDATE PRODUCT
    def build_product(self, vals):
        product = {
            'name': vals.get('description',''),
            'sf_id': vals.get('sf_id',''),
            'sf_pricebook_entry_id': vals.get('sf_pricebook_entry_id',''),
            'sf_pricebook_id': vals.get('sf_pricebook_id',''),
            'description_sale': vals.get('description_sale', ''),
            'description_purchase': vals.get('description_purchase', ''),
            'detailed_type': 'consu',
            'categ_id': 1,
            'list_price': vals.get('price_unit', 0.0),
            'standard_price': vals.get('standard_price', 0.0),
            'taxes_id': [(6, 0, [tax.id for tax in (vals.get('tax_id') or []) if hasattr(tax, 'id')])],
            'volume': vals.get('volume', 0.0),
            'weight': vals.get('weight', 0.0),
            'uom_id': vals.get('uom_id'),
            'uom_po_id': vals.get('uom_id'),
            'active': True,
            'company_id': self.company_id.id or self.env.company.id,
            }
        return product