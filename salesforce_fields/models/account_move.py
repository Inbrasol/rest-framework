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