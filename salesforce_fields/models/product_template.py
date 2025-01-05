from odoo import _, api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sf_id = fields.Char(string="Salesforce ID", index=True, unique=True)