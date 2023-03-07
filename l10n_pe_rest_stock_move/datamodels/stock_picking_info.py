# Copyright 2019 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from marshmallow import fields
from odoo.addons.datamodel.core import Datamodel
from odoo.addons.datamodel.fields import NestedModel

class StockPickingLine(Datamodel):
    _name = "stock.picking.line.info"

    product_id = fields.String(required=False, allow_none=True)
    name = fields.String(required=False, allow_none=True)
    product_uom = fields.String(required=False, allow_none=True)
    product_uom_qty = fields.Float(required=False, allow_none=True)

class StockPicking(Datamodel):
    _name = "stock.picking.info"
    name = fields.String(required=False, allow_none=False)
    state = fields.String(required=False, allow_none=False)
    id = fields.Integer(required=False, allow_none=False)
    l10n_pe_vat_code = fields.String(required=False, allow_none=False)
    vat = fields.String(required=False, allow_none=False)
    picking_type_code = fields.String(required=False, allow_none=False)
    picking_type_id = fields.String(required=False, allow_none=False)
    sale_id = fields.String(required=False, allow_none=False)
    origin = fields.String(required=False, allow_none=False)
    warehouse_ids =  fields.List(NestedModel("warehouse.info"))
    products = fields.List(NestedModel("stock.picking.line.info"))

class StockQuantList(Datamodel):
    _name = "stock.picking.list.info"
    count = fields.Integer(string="Rows")
    stock_picking = fields.List(NestedModel("stock.picking.info"))