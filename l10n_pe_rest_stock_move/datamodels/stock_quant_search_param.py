# Copyright 2019 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel
from odoo.addons.datamodel.fields import NestedModel

class StockQuantSearchParam(Datamodel):
    _name = "stock.quant.search.param"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=False)
    warehouse_ids =  fields.List(NestedModel("warehouse.info"))
    location_ids =  fields.List(NestedModel("location.info"))
    

class StockPickingSearchParam(Datamodel):
    _name = "stock.picking.search.param"
    id = fields.Integer(required=False, allow_none=False)
    l10n_pe_vat_code = fields.String(required=False, allow_none=False)
    vat = fields.String(required=False, allow_none=False)
    picking_type_code = fields.String(required=False, allow_none=False)
    picking_type_id = fields.String(required=False, allow_none=False)
    sale_id = fields.String(required=False, allow_none=False)
    origin = fields.String(required=False, allow_none=False)
    warehouse_ids =  fields.List(NestedModel("warehouse.info"))
    products = fields.List(NestedModel("stock.picking.line.info"))