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
    sf_owner_id = fields.Many2one('salesforce.user', string='Salesforce Owner')

    def create(self, vals):
        if 'sf_owner_id' not in vals and self.sale_order_id.sf_owner_id:
            vals['sf_owner_id'] = self.sale_order_id.sf_owner_id.id
        return super(AccountMove, self).create(vals)
    


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