from odoo import _, api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    sf_id = fields.Char(string="Salesforce ID", index=True, unique=True)
    #skip_sync = fields.Boolean(string='Skip Sync', default=False, copy=False)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    sf_id = fields.Char(string="Salesforce ID", index=True, unique=True)
    #skip_sync = fields.Boolean(string='Skip Sync', default=False, copy=False)