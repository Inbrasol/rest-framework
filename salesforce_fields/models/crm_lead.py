
from odoo import _, api, fields, models

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    sf_id = fields.Char(string="Salesforce ID", index=True, unique=True)