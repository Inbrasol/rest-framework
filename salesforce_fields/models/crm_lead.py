
from odoo import _, api, fields, models
from odoo.exceptions import UserError

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
    sf_owner_id = fields.Many2one('salesforce.user', string='Salesforce Owner')
    source_system = fields.Selection([
        ('salesforce', 'Salesforce'),
        ('odoo', 'Odoo')
    ], string='Source System', default='odoo',
    help="System from which the lead was created")

    def _get_salesforce_base_url(self):
        """Get Salesforce base URL from backend configuration"""
        backend = self.env['salesforce.backend'].search([('active', '=', True)], limit=1)
        if backend:
            # Extract the instance URL from the backend
            # For production: https://yourinstance.salesforce.com
            # For sandbox: https://yourinstance--sandbox.salesforce.com
            auth_response = backend.authenticate()
            instance_url = auth_response.get('instance_url', backend.url)
            return instance_url
        return None

    def action_open_in_salesforce(self):
        """Open the record in Salesforce"""
        self.ensure_one()
        if not self.sf_id:
            raise UserError(_("This record is not synchronized with Salesforce."))

        base_url = self._get_salesforce_base_url()
        if not base_url:
            raise UserError(_("Salesforce backend is not configured."))

        # Salesforce Lightning URL format: https://instance.lightning.force.com/lightning/r/Opportunity/RECORD_ID/view
        salesforce_url = f"{base_url}/lightning/r/Opportunity/{self.sf_id}/view"

        return {
            'type': 'ir.actions.act_url',
            'url': salesforce_url,
            'target': 'new',
        }

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
            'active': True
            }
        return product