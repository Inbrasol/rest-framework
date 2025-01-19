
from odoo import _, api, fields, models

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    sf_id = fields.Char(string="Salesforce ID", index=True, unique=True)
    #skip_sync = fields.Boolean(string='Skip Sync', default=False, copy=False)
    
class CrmLeadProduct(models.Model):
    _inherit = 'crm.lead.product'

    sf_id = fields.Char(string="Salesforce ID", index=True, unique=True)
    #skip_sync = fields.Boolean(string='Skip Sync', default=False, copy=False)