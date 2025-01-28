from odoo import _, api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sf_pricebook_entry_id = fields.Char(string="Price Book Entry ID", index=True, unique=True)
    sf_pricebook_id = fields.Char(string="Price Book ID", index=True, unique=True)
    sf_id = fields.Char(string='Salesforce ID', index=True, unique=True)
    sf_integration_status = fields.Selection([
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed')
    ], string='Integration Status', default='pending', help="Status of the Salesforce integration")
    sf_integration_datetime = fields.Datetime(string='Integration Datetime')
    sf_integration_error = fields.Text(string='Integration Error')