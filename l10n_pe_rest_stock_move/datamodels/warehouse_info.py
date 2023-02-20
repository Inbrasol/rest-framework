# Copyright 2019 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from marshmallow import fields
from odoo.addons.datamodel.core import Datamodel

class WarehouseInfo(Datamodel):
    _name = "warehouse.info"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=False)
