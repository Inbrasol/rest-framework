# Copyright 2019 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel
from odoo.addons.datamodel.fields import NestedModel

class SaleOrderLineInfo(Datamodel):
    _name = "sale.order.line.info"
    
    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=True, allow_none=False)
    product_id = fields.String(required=True, allow_none=False)
    product_uom = fields.String(required=True, allow_none=False)
    product_uom_qty = fields.Float(required=True, allow_none=False)
    price_unit = fields.Float(required=True, allow_none=False)
    analytic_line_ids = fields.List(NestedModel("analytic.info")) 
    analytic_tag_ids = fields.List(NestedModel("analytic.info")) 
    analytic_dimension_ids = fields.List(NestedModel("analytic.info")) 
    tax_id = fields.List(NestedModel("taxes.info")) 