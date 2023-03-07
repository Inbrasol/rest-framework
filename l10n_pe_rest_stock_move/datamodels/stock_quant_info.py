# Copyright 2019 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from marshmallow import fields
from odoo.addons.datamodel.core import Datamodel
from odoo.addons.datamodel.fields import NestedModel

class StockQuant(Datamodel):
    _name = "stock.quant.info"

    id = fields.Integer(required=False, allow_none=True)
    name = fields.String(required=False, allow_none=True)
    available_quantity = fields.Float(required=False, allow_none=True)
    reserved_quantity = fields.Float(required=False, allow_none=True)
    in_date = fields.DateTime(required=False, allow_none=True)
    location_id = fields.String(required=False, allow_none=True)
    warehouse_id = fields.String(required=False, allow_none=True)
    on_hand = fields.Boolean(required=False, allow_none=True)
    product_categ_id = fields.String(required=False, allow_none=True)
    product_id = fields.String(required=False, allow_none=True)
    product_name = fields.String(required=False, allow_none=True)
    product_uom_id = fields.String(required=False, allow_none=True)
    quantity = fields.Float(required=False, allow_none=True)
    tracking = fields.String(required=False, allow_none=True)



class StockQuantList(Datamodel):

    _name = "stock.quant.list.info"
    count = fields.Integer(string="Rows")
    stock_quants = fields.List(NestedModel("stock.quant.info"))