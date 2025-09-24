from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

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
    sf_owner_id = fields.Many2one('salesforce.user', string='Salesforce Owner')

    @api.model
    def default_get(self, fields_list):
        res = super(SaleOrder, self).default_get(fields_list)
        if 'sf_owner_id' in fields_list:
            opportunity = self.env.context.get('default_opportunity_id')
            if opportunity:
                opp = self.env['crm.lead'].browse(opportunity)
                if opp and opp.sf_owner_id:
                    res['sf_owner_id'] = opp.sf_owner_id.id
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
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