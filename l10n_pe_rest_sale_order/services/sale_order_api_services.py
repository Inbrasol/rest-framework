# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_datamodel.restapi import Datamodel
from odoo.addons.component.core import Component

class ProductApiService(Component):
    _inherit = "base.rest.service"
    _name = "sale.order.new_api.service"
    _usage = "sale_order"
    _collection = "l10n_pe.sale.order.rest.public.services"
    _description = """
        product New API Services
        Services developed with the new api provided by base_rest
    """
    
    @restapi.method(
        [(["/create"], "POST")],
        input_param=Datamodel("sale.order.search.param"),
        output_param=Datamodel("sale.order.info"),
        auth="public",
    )
    def create(self, product_category_param):
        """
        Search for products
        :param product_search_param: An instance of product.search.param
        :return: List of product.short.info
        """
        partner_search = self._get_by_document_type(product_category_param.get("l10n_pe_vat_code"),product_category_param.get("vat"))
        currrency = self.env["res.currency"].search([('name', '=',product_category_param.currency_id)],limit=1)
        create_params = {
            "partner_id": partner_search.id,
            "date_order": product_category_param.date_order,
            "origin":product_category_param.origin,
            "currency_id": currrency.id
        }
        #sale_order = self.env["sale.order"].create(self._prepare_params(create_params))


    def _get_by_document_type(self,_l10n_pe_vat_code,_vat):
        domain_partner = []
        domain_partner.append(("vat", "=", _vat))
        #Identification Type
        domain_identification = []
        domain_identification.append(("l10n_pe_vat_code", "=", _l10n_pe_vat_code))
        identification_type = self.env["l10n_latam.identification.type"].search(domain_identification,limit=1)
        if identification_type:
            domain_partner.append(("l10n_latam_identification_type_id","=", identification_type.id))
        return self.env["res.partner"].search(domain_partner)

    def _get_l10n_latam_identification(self,_l10n_pe_vat_code):
        domain_identification = []
        domain_identification.append(("l10n_pe_vat_code", "=", _l10n_pe_vat_code))
        return self.env["l10n_latam.identification.type"].search(domain_identification,limit=1)