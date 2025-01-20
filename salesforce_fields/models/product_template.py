from odoo import _, api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sf_id = fields.Char(string="Salesforce ID", index=True, unique=True)
    sf_pricebook_entry_id = fields.Char(string="Price Book Entry ID", index=True, unique=True)
    sf_pricebook_id = fields.Char(string="Price Book ID", index=True, unique=True)