# Copyright 2019 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel
from odoo.addons.datamodel.fields import NestedModel

class ProductSearchParam(Datamodel):
    _name = "product.search.param"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=False)
    last_update =  fields.DateTime(string="Ultima Modificación en")
    create_date = fields.DateTime(string="Creado en	")

class ProductCategorySearchParam(Datamodel):
    _name = "product.category.search.param"
    categories = fields.List(NestedModel("product.category.info"))
    parent_categories = fields.List(NestedModel("product.category.info"))
    last_update_start =  fields.Date(string="Ultima Modificación en")
    last_update_end =  fields.Date(string="Ultima Modificación en")
    create_date_start = fields.Date(string="Creado en")
    create_date_end = fields.Date(string="Creado en")

