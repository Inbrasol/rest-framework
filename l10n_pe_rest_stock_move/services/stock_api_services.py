# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_datamodel.restapi import Datamodel
from odoo.addons.component.core import Component


class ProductApiService(Component):
    _inherit = "base.rest.service"
    _name = "stock.new_api.service"
    _usage = "stock"
    _collection = "l10n_pe.stock.rest.public.services"
    _description = """
        product New API Services
        Services developed with the new api provided by base_rest
    """

    @restapi.method(
        [(["/stockquant"], "POST")],
        input_param=Datamodel("stock.quant.search.param"),
        output_param=Datamodel("stock.quant.list.info"),
        auth="public",
    )
    def get_stockquant(self, stock_quant_input):
        warehouse_names = []
        for warehouse in stock_quant_input.warehouse_ids:
            warehouse_names.append(warehouse.name)

        warehouse_ids = []
        location_names = []
        for warehouse in self.env["stock.warehouse"].search([('name', 'in', warehouse_names)]):
            warehouse_ids.append(warehouse.id)
            location_names.append(warehouse.code+"/Stock")

        location_ids = []
        for location in self.env["stock.location"].search([('warehouse_id', 'in', warehouse_ids),("usage", "=", "internal"),("complete_name","in",location_names)]):
            location_ids.append(location.id)

        stock_quants = self.env["stock.quant"].search(
            [('location_id', 'in', location_ids)])

        stockQuantInfo = self.env.datamodels["stock.quant.list.info"]
        res = stockQuantInfo(partial=True)
        res.count = len(stock_quants)
        res_stockquant = []
        for stock_quant_item in stock_quants:
            stockquantItemInfo = self.env.datamodels["stock.quant.info"]
            stockquant = stockquantItemInfo(partial=True)
            stockquant.product_id = stock_quant_item.product_id.code if stock_quant_item.product_id.code else ""
            stockquant.product_name = stock_quant_item.product_id.name
            stockquant.product_uom_id = stock_quant_item.product_uom_id.name if stock_quant_item.product_uom_id else ""
            stockquant.product_categ_id = stock_quant_item.product_categ_id.name if stock_quant_item.product_categ_id else ""
            stockquant.available_quantity = stock_quant_item.available_quantity
            stockquant.reserved_quantity = stock_quant_item.reserved_quantity
            stockquant.in_date = stock_quant_item.in_date
            #stockquant.warehouse_id = stock_quant_item.location_id.warehouse_id.name if  stock_quant_item.location_id else ""
            stockquant.quantity = stock_quant_item.quantity
            res_stockquant.append(stockquant)
        res.stock_quants = res_stockquant
        return res

    @restapi.method(
        [(["/stockpicking"], "POST")],
        input_param=Datamodel("stock.picking.search.param"),
        output_param=Datamodel("stock.picking.info"),
        auth="public",
    )
    def create_stockpicking(self, stock_picking_input):
        warehouse_names = []
        for warehouse in stock_picking_input.warehouse_ids:
            warehouse_names.append(warehouse.name)

        warehouse_ids = []
        for warehouse in self.env["stock.warehouse"].search([('name', 'in', warehouse_names)]):
            warehouse_ids.append(warehouse.id)
        partner_search = self._get_by_document_type(
            stock_picking_input.l10n_pe_vat_code, stock_picking_input.vat)
        stock_picking_type = self.env["stock.picking.type"].search(
            [('warehouse_id', 'in', warehouse_ids), ("sequence_code", "=", stock_picking_input.picking_type_code)])
        #location_id = self.env["stock.location"].search(
        #    [('warehouse_id', 'in', warehouse_ids), ("usage", "=", "internal")], limit=1)
        create_params = {
            "partner_id": partner_search.id,
            # date_order": product_category_param.date_order,
            "location_id": stock_picking_type.default_location_src_id.id,
            "location_dest_id": stock_picking_type.default_location_dest_id.id,
            "origin": stock_picking_input.origin,
            "picking_type_id": stock_picking_type.id
        }
        print("create_params----------------------")
        print(create_params)
        stock_picking = self.env["stock.picking"].create(create_params)
        stockPickingInfo = self.env.datamodels["stock.picking.info"]
        res = stockPickingInfo(partial=True)
        res.name = stock_picking.name
        res.picking_type_id = stock_picking.picking_type_id.name
        res.origin = stock_picking.origin
        res.l10n_pe_vat_code = stock_picking.partner_id.l10n_latam_identification_type_id.l10n_pe_vat_code
        res.vat = stock_picking.partner_id.vat

        #res_stockPicking = []
        """
        for stock_Picking_item in stock_Pickings :
            stockPickingItemInfo = self.env.datamodels["stock.Picking.info"]
            stockPicking = stockPickingItemInfo(partial=True)
            stockPicking.product_id = stock_Picking_item.product_id
            stockPicking.product_uom_id = stock_Picking_item.product_uom_id.code if stock_Picking_item.product_uom_id else ""
            stockPicking.product_categ_id = stock_Picking_item.product_categ_id.name if stock_Picking_item.product_categ_id else ""
            stockPicking.available_Pickingity = stock_Picking_item.available_Pickingity
            stockPicking.reserved_Pickingity = stock_Picking_item.reserved_Pickingity
            stockPicking.in_date = stock_Picking_item.in_date
            #stockPicking.warehouse_id = stock_Picking_item.location_id.warehouse_id.name
            stockPicking.Pickingity = stock_Picking_item.Pickingity
            res_stockPicking.append(stockPicking)
        res.stock_Pickings = res_stockPicking
        """
        return res

    def _get_by_document_type(self, _l10n_pe_vat_code, _vat):
        domain_partner = []
        domain_partner.append(("vat", "=", _vat))
        # Identification Type
        domain_identification = []
        domain_identification.append(("l10n_pe_vat_code", "=", _l10n_pe_vat_code))
        identification_type = self.env["l10n_latam.identification.type"].search(
            domain_identification, limit=1)
        if identification_type:
            domain_partner.append(
                ("l10n_latam_identification_type_id", "=", identification_type.id))
        return self.env["res.partner"].search(domain_partner)
