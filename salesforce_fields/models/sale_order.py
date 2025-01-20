from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sf_id = fields.Char(string="Salesforce ID", index=True, unique=True)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sf_id = fields.Char(string="Salesforce ID", index=True, unique=True)