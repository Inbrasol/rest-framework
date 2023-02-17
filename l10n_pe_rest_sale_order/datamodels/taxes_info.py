# Copyright 2019 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel


class StateInfo(Datamodel):
    _name = "taxes.info"

    id = fields.Integer(required=True, allow_none=True)
    name = fields.String(required=False, allow_none=True)
    amount = fields.Float(required=False, allow_none=True)
    l10n_pe_edi_tax_code = fields.String(required=False, allow_none=True)
