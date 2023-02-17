# Copyright 2019 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel
from odoo.addons.datamodel.fields import NestedModel


class ProductInfo(Datamodel):
    _name = "product.info"
    _inherit = "product.short.info"

    categ_id = fields.String(required=False, allow_none=True)
    description = fields.String(required=False, allow_none=True)
    price = fields.Float(required=False, allow_none=True)
    code = fields.String(required=False, allow_none=True)
    sale_ok = fields.Boolean(required=False, allow_none=True)
    purchase_ok = fields.Boolean(required=False, allow_none=True)
    uom_id = fields.String(required=False, allow_none=True)
    detailed_type = fields.String(required=False, allow_none=True)
    standard_price = fields.Float(required=False, allow_none=True)
    cost_method = fields.String(required=False, allow_none=True)
    taxes_id = fields.List(NestedModel("taxes.info"))
    l10n_pe_edi_is_for_advance = fields.Boolean(required=False, allow_none=True)
    l10n_pe_edi_product_code_id = fields.String(required=False, allow_none=True)
    active = fields.Boolean(required=False, allow_none=False)

    
class ProductCategoryInfo(Datamodel):
    _name = "product.bycategory.info"
    count = fields.Integer(string="Rows")
    products = fields.List(NestedModel("product.info"))