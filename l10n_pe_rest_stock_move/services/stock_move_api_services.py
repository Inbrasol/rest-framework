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
    _log_calls_in_db = True
    @restapi.method(
        [(["/stockpicking"], "POST")],
        input_param=Datamodel("stock.picking.search.param"),
        output_param=Datamodel("stock.quant.list.info"),
        auth="public",
    )
    def create_stockpicking(self, stock_picking_input):
        warehouse_names = []
        for warehouse in stock_picking_input.warehouse :
            warehouse_names.append(warehouse.name)
        
        warehouse_ids = []
        for warehouse in  self.env["stock.warehouse"].search([('name','in',warehouse_names)]):
            warehouse_ids.append(warehouse.id)
       
        #location_ids = []
        #for location in self.env["stock.location"].search([('warehouse_id','in',warehouse_ids)]):
        #    location_ids.append(location.id)
        
        #stock_quants = self.env["stock.quant"].search([('location_id','in',location_ids)])

        stockQuantInfo = self.env.datamodels["stock.picking.list.info"]
        res = stockQuantInfo(partial=True)
        #res.count = len(stock_quants)   
        res_stockquant = []
        """
        for stock_quant_item in stock_quants :
            stockquantItemInfo = self.env.datamodels["stock.quant.info"]
            stockquant = stockquantItemInfo(partial=True)
            stockquant.product_id = stock_quant_item.product_id
            stockquant.product_uom_id = stock_quant_item.product_uom_id.code if stock_quant_item.product_uom_id else ""
            stockquant.product_categ_id = stock_quant_item.product_categ_id.name if stock_quant_item.product_categ_id else ""
            stockquant.available_quantity = stock_quant_item.available_quantity
            stockquant.reserved_quantity = stock_quant_item.reserved_quantity
            stockquant.in_date = stock_quant_item.in_date
            #stockquant.warehouse_id = stock_quant_item.location_id.warehouse_id.name
            stockquant.quantity = stock_quant_item.quantity
            res_stockquant.append(stockquant)
        res.stock_quants = res_stockquant
        """
        return res