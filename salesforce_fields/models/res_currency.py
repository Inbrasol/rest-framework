# Copyright 2016 Antonio Espinosa
# Copyright 2020 Tecnativa - João Marques
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResCurrency(models.Model):
    _inherit = "res.currency"

    sf_pricebook_entry_id = fields.Char(string="SF Pricebook Entry ID", index=True, unique=True)