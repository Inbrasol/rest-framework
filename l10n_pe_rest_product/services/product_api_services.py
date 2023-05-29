# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_datamodel.restapi import Datamodel
from odoo.addons.component.core import Component


class ProductApiService(Component):
    _inherit = "base.rest.service"
    _name = "product.new_api.service"
    _usage = "product"
    _collection = "l10n_pe.product.rest.public.services"
    _description = """
        product New API Services
        Services developed with the new api provided by base_rest
    """
    _log_calls_in_db = True
    @restapi.method(
        [(["/<int:id>/get", "/<int:id>"], "GET")],
        output_param=Datamodel("product.info"),
        auth="user",
    )
    def get(self, _id):
        """
        Get product's information
        """
        product = self._get(_id)
        productInfo = self.env.datamodels["product.info"]
        product_info = productInfo(partial=True)
        product_info.name = product.name
        product_info.id = product.id
        product_info.categ_id = product.categ_id.name
        product_info.description = product.description
        product_info.price = product.price
        product_info.code = product.code
        product_info.sale_ok = product.sale_ok
        product_info.purchase_ok = product.purchase_ok
        product_info.uom_id = product.uom_id.name
        product_info.detailed_type = product.detailed_type
        product_info.standard_price = product.standard_price
        product_info.cost_method = product.cost_method
        product_info.taxes_id = product.taxes_id
        product_info.l10n_pe_edi_is_for_advance = product.l10n_pe_edi_is_for_advance
        product_info.l10n_pe_edi_product_code_id = product.l10n_pe_edi_product_code_id.name
        product_info.active = product.active
        return product_info

    @restapi.method(
        [(["/get_by_category"], "POST")],
        input_param=Datamodel("product.category.search.param"),
        output_param=Datamodel("product.bycategory.info"),
        auth="public",
    )
    def search(self, product_category_param):
        """
        Search for products
        :param product_search_param: An instance of product.search.param
        :return: List of product.short.info
        """
        print("-------product_search_param---------")
        print(product_category_param)
        if product_category_param:
            category_names=[]
            categories_ids = []
            if product_category_param.categories and len(product_category_param.categories)>0:
                # CATEORIES
                for category in product_category_param.categories:
                    category_names.append(category.name)
                categories_query = self.env["product.category"].search([('name','in',category_names)])
                for category  in categories_query:
                    categories_ids.append(category.id)
            if product_category_param.parent_categories and len(product_category_param.parent_categories)>0:
                #PARENT_CATEGORIES
                parent_category_names=[]
                for category in product_category_param.parent_categories:
                    parent_category_names.append(category.name)
                parent_categories_query = self.env["product.category"].search([('name','in',parent_category_names)])
                for category  in parent_categories_query.child_id:
                    categories_ids.append(category.id)

            products = []
            if product_category_param.last_update_start and product_category_param.last_update_end and product_category_param.create_date_start and product_category_param.create_date_end:
                products = self.env["product.product"].search(
                    [
                    ('categ_id','in',categories_ids),
                    ('__last_update', '>=',product_category_param.last_update_start),
                    ('__last_update', '<=',product_category_param.last_update_end),
                    ('create_date', '>=',product_category_param.create_date_start),
                    ('create_date', '<=',product_category_param.create_date_end)
                    ])

            elif product_category_param.last_update_start and product_category_param.last_update_end:
                 products = self.env["product.product"].search(
                    [
                    ('categ_id','in',categories_ids),
                    ('__last_update', '>=',product_category_param.last_update_start),
                    ('__last_update', '<=',product_category_param.last_update_end)
                    ])

            elif product_category_param.create_date_start and product_category_param.create_date_end :
                 products = self.env["product.product"].search(
                    [
                    ('categ_id','in',categories_ids),
                    ('create_date', '>=',product_category_param.create_date_start),
                    ('create_date', '<=',product_category_param.create_date_end)
                    ])
            else:
                 products = self.env["product.product"].search([('categ_id','in',categories_ids)])
            
            productsCatInfo = self.env.datamodels["product.bycategory.info"]
            res = productsCatInfo(partial=True)
            res.count = len(products)
            res_products = []
            for product in products:
                productInfo = self.env.datamodels["product.info"]
                product_info = productInfo(partial=True)
                product_info.name = product.name
                product_info.id = product.id
                product_info.categ_id = product.categ_id.name
                product_info.description = product.description
                product_info.price = product.price
                product_info.code = product.code
                product_info.sale_ok = product.sale_ok
                product_info.purchase_ok = product.purchase_ok
                product_info.uom_id = product.uom_id.name
                product_info.detailed_type = product.detailed_type
                product_info.standard_price = product.standard_price
                product_info.cost_method = product.cost_method
                #product_info.taxes_id = product.taxes_id
                #tax
                taxes = []
                for tax in product.taxes_id:
                    TaxInfo = self.env.datamodels["taxes.info"]
                    tax_info = TaxInfo(partial=True)
                    tax_info.id = tax.id
                    tax_info.name = tax.name
                    tax_info.amount = tax.amount
                    tax_info.l10n_pe_edi_tax_code= tax.l10n_pe_edi_tax_code
                    taxes.append(tax_info)
                product_info.taxes_id = taxes
                product_info.l10n_pe_edi_is_for_advance = product.l10n_pe_edi_is_for_advance
                product_info.l10n_pe_edi_product_code_id = product.l10n_pe_edi_product_code_id.name
                product_info.active = product.active

                res_products.append(product_info)
            res.products = res_products
            print("res-last")
            print(res)
        return res

    # The following method are 'private' and should be never never NEVER call
    # from the controller.

    def _get(self, _id):
        return self.env["product.product"].browse(_id)

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
                "l10n_pe_edi_product_code_id": product.l10n_pe_edi_product_code_id.name,
                "active": product.active
            }
        print(res)
        return res