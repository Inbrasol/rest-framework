from odoo import models, fields

class SalesforceUser(models.Model):
    _name = 'salesforce.user'
    _description = 'Salesforce User'

    name = fields.Char(string='Name', required=True)
    user_id = fields.Many2one('res.users', string='User', required=True)
    approval_user_id = fields.Many2one('res.users', string='Approval User')
    partner_id = fields.Many2one('res.partner', string='Partner',related='user_id.partner_id', store=True)
    sf_id = fields.Char(string='Salesforce ID', required=True)
    sf_username = fields.Char(string='Salesforce Username', required=True)
    active = fields.Boolean(string='Active', default=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')