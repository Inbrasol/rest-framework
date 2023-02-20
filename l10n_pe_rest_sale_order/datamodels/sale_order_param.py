# Copyright 2019 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel
from odoo.addons.datamodel.fields import NestedModel

class SaleSearchParam(Datamodel):
    _name = "sale.order.search.param"
    name = fields.String(required=False, allow_none=False)
    type_name =  fields.String(required=True, allow_none=False)
    l10n_pe_vat_code =  fields.String(required=True, allow_none=False)
    vat =  fields.String(required=True, allow_none=False)
    date_order =  fields.String(required=True, allow_none=False)
    payment_term_id =  fields.String(required=False, allow_none=False)
    origin = fields.String(required=False, allow_none=False)
    currency_id = fields.String(required=True, allow_none=False)
    lines =  fields.List(NestedModel("sale.order.line.info")) 