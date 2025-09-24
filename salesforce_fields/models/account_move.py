from odoo import _, api, fields, models

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
    sf_retry_count = fields.Integer(string='Retry Count', default=0)
    sf_last_sync_attempt = fields.Datetime(string='Last Sync Attempt')
    sf_error_code = fields.Char(string='Error Code')

    def _get_sf_owner_id(self):
        if self.sale_order_id and self.sale_order_id.sf_owner_id:
            return self.sale_order_id.sf_owner_id.id
        return False

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
    sf_retry_count = fields.Integer(string='Retry Count', default=0)
    sf_last_sync_attempt = fields.Datetime(string='Last Sync Attempt')
    sf_error_code = fields.Char(string='Error Code')