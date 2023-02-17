# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo.addons.base_rest.components.service import to_bool, to_int
from odoo.addons.component.core import Component
from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_datamodel.restapi import Datamodel


class productService(Component):
    _inherit = "base.rest.service"
    _name = "product.service"
    _usage = "product"
    _collection = "l10n_pe.product.rest.private.services"
    _description = """
        product Services
        Access to the product services is only allowed to authenticated users.
        If you are not authenticated go to <a href='/web/login'>Login</a>
    """

    def get(self, _id):
        """
        Get product's informations
        """
        print("Alll")
        return self._to_json(self._get(_id))
    
    @restapi.method(
        [(["/get_by_category"], "GET")],
        input_param = Datamodel("product.category.info"),
        output_param = Datamodel("product.info", is_list=True),
        auth="user",
    )
    def get(self, _categories):
        """
        Get product's informations
        """
        print("All")
        return self._get_by_categories(_categories)

    """
    @restapi.method(
        [(["/", "/get_by_category"], "GET")],
        input_param = Datamodel("product.category.info"),
        output_param = Datamodel("product.info", is_list=True),
        auth="user",
    )
    def get_by_category(self, **params):
        
        print("param-----------------")
        print(params)
        if params:
            categories_names = params.get("name").split()
            #categories = []
            #for param in params:
            #    categories.append(param.name)
            #domain = []
            category = self.env["product.category"].search([('name', 'in',categories_names)])
            #for param in params:
            #    domain.append(("active","=",True))
            products = self.env["product.product"].search([('category_id', 'in' ,category.child_id)])
            #products = self.env["product.product"].browse([i[0] for i in products])
            rows = []
            print(products)
            res = {"count": len(products), "rows": rows}
            for product in products:
                rows.append(self._to_json(product))
        return res
    def search(self, **params):
        products = self.env["product.product"].serach(name)
        products = self.env["product.product"].browse([i[0] for i in products])
        rows = []
        res = {"count": len(products), "rows": rows}
        for product in products:
            rows.append(self._to_json(product))
        return res
    """
    """"
    def create(self, **params):
        product = self.env["product.product"].create(self._prepare_params(params))
        return self._to_json(product)

    def update(self, _id, **params):
        product = self._get(_id)
        product.write(self._prepare_params(params))
        return self._to_json(product)

    def archive(self, _id, **params):
        return {"response": "Method archive called with id %s" % _id}
    """
    
    def _get(self, _id):
        return self.env["product.product"].browse(_id)

    def _get_by_categories(self, _categories):
        res = []
        if _categories:
            #categories = _categories
            #print("categories")
            #print(categories)
            category = self.env["product.category"].search([('name','=',"All")])
            print("-------------category--------")
            print(category)
            query_categ = []
            for category  in category.child_id:
                query_categ.append(category.id)
            products = self.env["product.product"].search([('categ_id', 'in',query_categ)])
            rows = []
            #print(products)
            #res = products
            res = {"count": len(products), "rows": rows}
            print("res")
            print(res)
            for product in products:
                rows.append(self._to_json(product))
        return res

    def _prepare_params(self, params):
        for key in ["country", "state"]:
            if key in params:
                val = params.pop(key)
                if val.get("id"):
                    params["%s_id" % key] = val["id"]
        return params

    # Validator

    def _validator_return_get(self):
        #res = self._validator_create()
        return {
            "count": {"type": "integer", "required": False},
            "rows": {
                "type": "list",
                "required": False,
                "schema": {"type": "dict", "schema": self._validator_return_get()},
            },
        }
    """
    def _validator_search(self):
        return {"name": {"type": "string", "nullable": False, "required": True}}

    def _validator_return_search(self):
        return {
            "count": {"type": "integer", "required": True},
            "rows": {
                "type": "list",
                "required": True,
                "schema": {"type": "dict", "schema": self._validator_return_get()},
            },
        }

    def _validator_create(self):
        res = {
            "name": {"type": "string", "required": False, "empty": False},
        }
        return res

    def _validator_return_create(self):
        return self._validator_return_get()

    def _validator_update(self):
        res = self._validator_create()
        for key in res:
            if "required" in res[key]:
                del res[key]["required"]
        return res

    def _validator_return_update(self):
        return self._validator_return_get()

    def _validator_archive(self):
        return {}

    """
    def _to_json(self, product):
        res = {
                "id": product.id,
                "name": product.name,
                "categ_id": product.categ_id.name,
                "description":product.description,
                "price": product.price,
                "code": product.code,
                "sale_ok": product.sale_ok,
                "purchase_ok":product.purchase_ok,
                "uom_id": product.uom_id.name,
                "detailed_type": product.detailed_type,
                "standard_price": product.standard_price,
                "cost_method": product.cost_method,
                #"taxes_id": product.taxes_id.name,
                "l10n_pe_edi_is_for_advance": product.l10n_pe_edi_is_for_advance,
                "l10n_pe_edi_product_code_id": product.l10n_pe_edi_product_code_id,
                "active": product.active
            }
        print(res)
        return res