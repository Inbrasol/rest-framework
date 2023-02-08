# Copyright 2019 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel
from odoo.addons.datamodel.fields import NestedModel


class PartnerInfo(Datamodel):
    _name = "l10n_pe.partner.info"
    _inherit = "l10n_pe.partner.short.info"
    company_type = fields.String(required=False, allow_none=False)
    l10n_latam_identification_type_id = fields.String(required=False, allow_none=False)
    vat = fields.String(required=False, allow_none=False)
    email = fields.String(required=False, allow_none=False)
    street = fields.String(required=False, allow_none=False)
    street2 = fields.String(required=False, allow_none=True)
    zip_code = fields.String(required=False, allow_none=False)
    city = fields.String(required=False, allow_none=False)
    phone = fields.String(required=False, allow_none=True)
    website = fields.String(required=False, allow_none=True)
    title = fields.String(required=False, allow_none=True)
    category_id = fields.String(required=False, allow_none=True)
    state = NestedModel("l10n_pe.state.info")
    country = NestedModel("l10n_pe.country.info")
    l10n_latam_identification_type = NestedModel("l10n_latam.identification.type.info")
    is_company = fields.Boolean(required=False, allow_none=False)
