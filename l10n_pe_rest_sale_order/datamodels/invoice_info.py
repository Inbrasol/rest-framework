# Copyright 2019 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel


class CountryInfo(Datamodel):
    _name = "invoice.info"

    id = fields.Integer(required=False, allow_none=True)
    name = fields.String(required=True, allow_none=False)
    state = fields.String(required=False, allow_none=True)
    invoice_date = fields.String(required=False, allow_none=True)
    l10n_latam_document_type_id = fields.String(required=False, allow_none=True)
    l10n_pe_edi_sunat_accepted =  fields.Boolean(required=False, allow_none=True)