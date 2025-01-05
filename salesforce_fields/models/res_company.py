# Copyright 2016 Antonio Espinosa
# Copyright 2020 Tecnativa - João Marques
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResCompany(models.Model):
    _inherit = "res.company"

    sf_id = fields.Char(string="Salesforce ID", index=True, unique=True)