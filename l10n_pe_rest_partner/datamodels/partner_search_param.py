# Copyright 2019 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel


class PartnerSearchParam(Datamodel):
    _name = "l10n_pe.partner.search.param"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=False)
    l10n_latam_identification_type_id = fields.String(required=False, allow_none=False)
    vat = fields.String(required=False, allow_none=False)