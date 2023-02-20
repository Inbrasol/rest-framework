# Copyright 2019 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel
from odoo.addons.datamodel.fields import NestedModel

class StockQuantSearchParam(Datamodel):
    _name = "stock.quant.search.param"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=False)
    warehouse =  fields.List(NestedModel("warehouse.info"))
    location =  fields.List(NestedModel("location.info"))