from odoo import models, fields, api

class SalesforceUser(models.Model):
    _name = 'salesforce.user'

    name = fields.Char('Name', required=True)
    user_id = fields.Many2one('res.users', 'User', required=True)
    sf_id = fields.Char('Salesforce ID', required=True)
    sf_username = fields.Char('Salesforce Username', required=True)
    active = fields.Boolean('Active', default=True)
