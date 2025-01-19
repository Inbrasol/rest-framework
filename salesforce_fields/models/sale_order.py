from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sf_id = fields.Char(string="Salesforce ID", index=True, unique=True)
    #skip_sync = fields.Boolean(string='Skip Sync', default=False, copy=False)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sf_id = fields.Char(string="Salesforce ID", index=True, unique=True)
    #skip_sync = fields.Boolean(string='Skip Sync', default=False, copy=False)