from odoo import _, api, fields, models
from odoo.exceptions import UserError

class AccountMove(models.Model):

    _inherit = 'account.move'

    sf_id = fields.Char(string='Salesforce ID', index=True, unique=True)
    sf_integration_status = fields.Selection([
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed')
    ], string='Integration Status', default='pending', help="Status of the Salesforce integration")
    sf_integration_datetime = fields.Datetime(string='Integration Datetime')
    sf_integration_error = fields.Text(string='Integration Error')
    sf_owner_id = fields.Many2one('salesforce.user', string='Salesforce Owner', default=lambda self: self._get_sf_owner_id())

    def _get_sf_owner_id(self):
        if self.sale_order_id and self.sale_order_id.sf_owner_id:
            return self.sale_order_id.sf_owner_id.id
        return False

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

        # Salesforce Lightning URL format: https://instance.lightning.force.com/lightning/r/Invoice/RECORD_ID/view
        salesforce_url = f"{base_url}/lightning/r/Order/{self.sf_id}/view"

        return {
            'type': 'ir.actions.act_url',
            'url': salesforce_url,
            'target': 'new',
        }

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    sf_id = fields.Char(string='Salesforce ID', index=True, unique=True)
    sf_integration_status = fields.Selection([
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed')
    ], string='Integration Status', default='pending', help="Status of the Salesforce integration")
    sf_integration_datetime = fields.Datetime(string='Integration Datetime')
    sf_integration_error = fields.Text(string='Integration Error')