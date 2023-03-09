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
        [(["/get"], "GET")],
        input_param=Datamodel("sale.order.get.param"),
        output_param=Datamodel("sale.order.info"),
        auth="public",
    )
    def get(self, sale_order_search):
        sale_order = self.env["sale.order"].search([('name','=',sale_order_search.name)],limit=1)
        saleordeInfo = self.env.datamodels["sale.order.info"]
        res = saleordeInfo(partial=True)
        res.name = sale_order.name
        res.currency_id = sale_order.currency_id.name
        res.type_name = ""
        res.l10n_pe_vat_code = sale_order.partner_id.l10n_latam_identification_type_id.l10n_pe_vat_code
        res.date_order = sale_order.date_order
        res.vat = sale_order.partner_id.vat
        res.date_order = sale_order.date_order
        res.state = sale_order.state
        res.invoice_status = sale_order.invoice_status
        invoice_ids = []
        for invoice_item in sale_order.invoice_ids:
            saleordeInfo = self.env.datamodels["invoice.info"]
            invoice = saleordeInfo(partial=True)
            invoice.name = invoice_item.name
            invoice.state = invoice_item.state
            invoice.invoice_date = invoice_item.invoice_date
            #invoice.l10n_latam_document_type_id = invoice_item.l10n_latam_document_type_id.name
            invoice.l10n_pe_edi_sunat_accepted = invoice_item.l10n_pe_edi_sunat_accepted
            invoice_ids.append(invoice)
        res.invoice_ids = invoice_ids
        
        return res
    
    @restapi.method(
        [(["/update"], "PUT")],
        input_param=Datamodel("sale.order.search.param"),
        output_param=Datamodel("sale.order.info"),
        auth="public",
    )
    def update(self, product_category_param):
        sale_order = self.env["sale.order"].search([('name', '=',product_category_param.name)],limit=1)
        update_params = {
            "id": sale_order.id,
        }
        if product_category_param.currency_id:
            currrency = self.env["res.currency"].search([('name', '=',product_category_param.currency_id)],limit=1)
            product_pricelist =  self.env["product.pricelist"].search([('currency_id', '=',currrency.id)],limit=1)
            update_params["currency_id"] = currrency.id
            update_params["pricelist_id"] = product_pricelist.id

        if product_category_param.payment_term_id:
            payment_term =  self.env["account.payment.term"].search([('name', '=',product_category_param.payment_term_id)],limit=1)
            update_params["payment_term_id"] = payment_term.id
        
        if product_category_param.l10n_pe_vat_code and product_category_param.vat:
            partner_search = self._get_by_document_type(product_category_param.l10n_pe_vat_code,product_category_param.vat)
            update_params["partner_id"] = partner_search.id

        if product_category_param.date_order:
            update_params["date_order"] = product_category_param.date_order
        
        print("--------create_params---------")
        print(update_params)
        #lines
        sale_lines = []
        if product_category_param.lines:
            sale_order_line_ids = []
            for order_line in sale_order.order_line:
                sale_order_line_ids.append(order_line.id)
            sale_order_line_set = self.env['sale.order.line'].search([('id', 'in',sale_order_line_ids)])
            sale_order_line_set.unlink()
            
            for sale_line in product_category_param.lines:
                product = self.env["product.product"].search([('name','=',sale_line.name)],limit=1)
                #product =  self.env["product.template"].search([('default_code','in', sale_line.product_id)],limit=1)
                uom_id = self.env["uom.uom"].search([('name','=', sale_line.product_uom)],limit=1)
                print("---product_uom---")
                print(uom_id)
                """
            analytic_line = []
            if sale_line.analytic_line_ids:
                for analytic_line in sale_line.analytic_line_ids:
                    analytic_line.append(analytic_line.id)

            analytic_line_ids: self.env["​account.analytic.account"].search([('code', 'in',analytic_line)])

            tag_line = []
            if sale_line.analytic_tag_ids:
                for tag_line in sale_line.analytic_tag_ids:
                    tag_line.append(tag_line.name)
            analytic_tag_ids: self.env["​account.analytic.tag"].search([('name', 'in' ,tag_line)])
            """
                #taxes
                tax_name = []
                if sale_line.tax_id:
                    for tax in sale_line.tax_id:
                        tax_name.append(tax.name)
                tax_id = self.env["account.tax"].search([('name', 'in' ,tax_name)])
            
                sale_lines.append((0, 0,{
                    "product_id" : product.id,
                    "currency_id": currrency.id,
                    "name": sale_line.name,
                    "product_uom": uom_id.id,
                    "product_uom_qty": sale_line.product_uom_qty,
                    "price_unit":sale_line.price_unit,
                    #"tax_id":tax_id
                    #"analytic_line_ids":analytic_line_ids,
                    #"analytic_tag_ids":analytic_tag_ids
                }))
        
        update_params["order_line"] = sale_lines
        print("---------------update_params------")
        print(update_params)
        #res_sale_order = self.env["sale.order"].write(update_params)
        #self.env["sale.order"].write(update_params)
        res_sale_order = self.env["sale.order"].browse(sale_order.id)
        res_sale_order.write(update_params)
        #RETURN
        print("sale_order")
        print(res_sale_order)
        saleordeInfo = self.env.datamodels["sale.order.info"]
        res = saleordeInfo(partial=True)
        res.name = res_sale_order.name
        res.origin = res_sale_order.origin
        res.currency_id = res_sale_order.currency_id.name
        res.type_name = ""
        res.l10n_pe_vat_code = res_sale_order.partner_id.l10n_latam_identification_type_id.l10n_pe_vat_code
        res.vat = res_sale_order.partner_id.vat
        res.date_order = res_sale_order.date_order
        res.state = res_sale_order.state
        res.invoice_status = res_sale_order.invoice_status
        return res

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
        print("-------product_category_param------------")
        print(product_category_param)

        partner_search = self._get_by_document_type(product_category_param.l10n_pe_vat_code,product_category_param.vat)
        currrency = self.env["res.currency"].search([('name', '=',product_category_param.currency_id)],limit=1)
        payment_term =  self.env["account.payment.term"].search([('name', '=',product_category_param.payment_term_id)],limit=1)
        product_pricelist =  self.env["product.pricelist"].search([('currency_id', '=',currrency.id)],limit=1)
        create_params = {
            "partner_id": partner_search.id,
            "date_order": product_category_param.date_order,
            "origin":product_category_param.origin,
            "currency_id": currrency.id,
            "payment_term_id":payment_term.id,
            "pricelist_id" : product_pricelist.id
        }
        print("--------create_params---------")
        print(create_params)
        #lines
        sale_lines = []
        for sale_line in product_category_param.lines:
            product = self.env["product.product"].search([('name','=',sale_line.name)],limit=1)
            #product =  self.env["product.template"].search([('default_code','in', sale_line.product_id)],limit=1)
            product_uom = self.env["uom.uom"].search([('name','in',sale_line.product_uom)],limit=1)
            print("---product_uom---")
            print(product_uom)
            """
            analytic_line = []
            if sale_line.analytic_line_ids:
                for analytic_line in sale_line.analytic_line_ids:
                    analytic_line.append(analytic_line.id)

            analytic_line_ids: self.env["​account.analytic.account"].search([('code', 'in',analytic_line)])

            tag_line = []
            if sale_line.analytic_tag_ids:
                for tag_line in sale_line.analytic_tag_ids:
                    tag_line.append(tag_line.name)
            analytic_tag_ids: self.env["​account.analytic.tag"].search([('name', 'in' ,tag_line)])
            """
            #taxes
            tax_name = []
            if sale_line.analytic_tag_ids:
                for tax in sale_line.tax_id:
                    tax_name.append(tax.name)
            tax_id = self.env["account.tax"].search([('name', 'in' ,tax_name)])

            """
            sale_line = {
                "product_id" : product.id,
                "currency_id": currrency.id,
                "name": sale_line.name,
                "product_uom": 1,
                "product_uom_qty": sale_line.product_uom_qty,
                "price_unit":sale_line.price_unit,
                #"tax_id":tax_id
                #"analytic_line_ids":analytic_line_ids,
                #"analytic_tag_ids":analytic_tag_ids
            }
            """
            sale_lines.append((0, 0,{
                "product_id" : product.id,
                "currency_id": currrency.id,
                "name": sale_line.name,
                "product_uom": 5,
                "product_uom_qty": sale_line.product_uom_qty,
                "price_unit":sale_line.price_unit,
                #"tax_id":tax_id
                #"analytic_line_ids":analytic_line_ids,
                #"analytic_tag_ids":analytic_tag_ids
            }))
        create_params["order_line"] = sale_lines

        print("---------------create_params------")
        print(create_params)
        sale_order = self.env["sale.order"].create(create_params)
        print("sale_order")
        print(sale_order)
        saleordeInfo = self.env.datamodels["sale.order.info"]
        res = saleordeInfo(partial=True)
        res.name = sale_order.name
        res.origin = sale_order.origin
        res.currency_id = sale_order.currency_id.name
        res.type_name = product_category_param.type_name
        res.l10n_pe_vat_code =sale_order.partner_id.l10n_latam_identification_type_id.l10n_pe_vat_code
        res.vat = sale_order.partner_id.vat
        res.date_order = sale_order.date_order
        res.state = sale_order.state
        res.invoice_status = sale_order.invoice_status
        return res


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