# Copyright 2019 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel


class LatamIdentificationType(Datamodel):
    _name = "l10n_latam.identification.type.info"

    id = fields.Integer(required=True, allow_none=False)
    name = fields.String(required=True, allow_none=False)
    l10n_pe_vat_code = fields.String(required=False, allow_none=False)
