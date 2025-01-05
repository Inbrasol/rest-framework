from odoo import _, api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    sf_id = fields.Char(string="Salesforce ID", index=True, unique=True)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    sf_id = fields.Char(string="Salesforce ID", index=True, unique=True)