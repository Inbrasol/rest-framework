# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_datamodel.restapi import Datamodel
from odoo.addons.component.core import Component


class PartnerApiService(Component):
    _inherit = "base.rest.service"
    _name = "l10n_pe.partner.api.service"
    _usage = "partner"
    _collection = "l10n_pe.partner.rest.public.services"
    _description = """
        Partner New API Services
        Services developed with the new api provided by base_rest
    """

    @restapi.method(
        [(["/", "/search"], "GET")],
        input_param=Datamodel("l10n_pe.partner.search.param"),
        output_param=Datamodel("l10n_pe.partner.short.info", is_list=True),
        auth="public",
    )
    def search(self, partner_search_param):
        """
        Search for partners
        :param partner_search_param: An instance of partner.search.param
        :return: List of partner.short.info
        """
        domain = []
        if partner_search_param.name:
            domain.append(("name", "like", partner_search_param.name))
        if partner_search_param.id:
            domain.append(("id", "=", partner_search_param.id))
        if partner_search_param.vat:
            domain.append(("vat", "=", partner_search_param.vat))
        res = []
        PartnerInfo = self.env.datamodels["l10n_pe.partner.info"]
        for p in self.env["res.partner"].search(domain):
            res.append(PartnerInfo(
                id=p.id,
                name=p.name,
                #l10n_latam_identification_type_id = p.l10n_latam_identification_type_id.name,
                vat = p.vat,
                street = p.street,
                zip_code = p.zip,
                city = p.city,
                phone = p.phone,
                email = p.email,
                is_company = p.is_company,
                company_type = p.company_type,
                country = self.env.datamodels["l10n_pe.country.info"](id=p.country_id.id, name=p.country_id.name),
                state = self.env.datamodels["l10n_pe.state.info"](id=p.state_id.id, name=p.state_id.name),
                l10n_latam_identification_type =  self.env.datamodels["l10n_latam.identification.type.info"](id=p.l10n_latam_identification_type_id.id, name=p.l10n_latam_identification_type_id.name),
                website = p.website,
                ))
        return res

    def create(self, **params):
        """
        Create a new partner
        """
        partner = self.env["res.partner"].create(self._prepare_params(params))
        return self._to_json(partner)

    def update(self, _id, **params):
        """
        Update partner informations
        """
        partner = self._get(_id)
        partner.write(self._prepare_params(params))
        return self._to_json(partner)