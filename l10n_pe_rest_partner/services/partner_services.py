# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo.addons.base_rest.components.service import to_bool, to_int
from odoo.addons.component.core import Component
from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_datamodel.restapi import Datamodel

class PartnerService(Component):
    _inherit = "base.rest.service"
    _name = "l10n_pe.partner.service"
    _usage = "partner"
    _collection = "l10n_pe.partner.rest.private.services"
    _description = """
        Partner Services
        Access to the partner services is only allowed to authenticated users.
        If you are not authenticated go to <a href='/web/login'>Login</a>
    """

    def get(self, _id):
        """
        Get partner's informations
        """
        return self._to_json(self._get(_id))

    # pylint:disable=method-required-super
    def create(self, **params):
        """
        Create a new partner
        """
        #search before create
        
        if params.get("vat") and params.get("l10n_latam_identification_type_id"):
            domain_partner = []
            domain_partner.append(("vat", "=", params.get("vat")))
            #Identification Type
            domain_identification = []
            domain_identification.append(("l10n_pe_vat_code", "=", params.get("l10n_latam_identification_type_id")))
            identification_type = self.env["l10n_latam.identification.type"].search(domain_identification,limit=1)
            if identification_type:
                domain_partner.append(("l10n_latam_identification_type_id","=", identification_type.id))
                partner_search = self.env["res.partner"].search(domain_partner)
                return self._to_json(partner_search)
        #Create
        if not partner_search:
            partner = self.env["res.partner"].create(self._prepare_params(params))
            return self._to_json(partner)

 
    """@restapi.method(
        [(["/", "/update"], "GET")],
        input_param=Datamodel("l10n_pe.partner.search.param"),
        output_param=Datamodel("l10n_pe.partner.info", is_list=True),
        auth="public",
    )
    """
    def update(self,**params):
        """
        Update partner informations
        """
        partner = self._get_by_document_type(params.get("l10n_latam_identification_type_id"),params.get("vat"))
        partner.write(self._prepare_params(params))
        return self._to_json(partner)

    def archive(self, _id, **params):
        """
        Archive the given partner. This method is an empty method, IOW it
        don't update the partner. This method is part of the demo data to
        illustrate that historically it's not mandatory to defined a schema
        describing the content of the response returned by a method.
        This kind of definition is DEPRECATED and will no more supported in
        the future.
        :param _id:
        :param params:
        :return:
        """
        return {"response": "Method archive called with id %s" % _id}

    # The following method are 'private' and should be never never NEVER call
    # from the controller.

    def _get(self, _id):
        return self.env["res.partner"].browse(_id)
    
    def _get_by_document_type(self,_l10n_latam_identification_type_id,_vat):
        domain_partner = []
        domain_partner.append(("vat", "=", _vat))
        #Identification Type
        domain_identification = []
        domain_identification.append(("l10n_pe_vat_code", "=", _l10n_latam_identification_type_id))
        identification_type = self.env["l10n_latam.identification.type"].search(domain_identification,limit=1)
        if identification_type:
            domain_partner.append(("l10n_latam_identification_type_id","=", identification_type.id))
        return self.env["res.partner"].search(domain_partner)

    def _prepare_params(self, params):
        for key in ["country", "state","l10n_latam_identification_type"]:
            if key in params:
                val = params.pop(key)
                if val.get("id"):
                    params["%s_id" % key] = val["id"]
        return params

    # Validator
    def _validator_return_get(self):
        res = self._validator_create()
        res.update({"id": {"type": "integer", "required": True, "empty": False}})
        return res

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
            "name": {"type": "string", "required": True, "empty": False},
            "l10n_latam_identification_type_id": {"type": "string", "required": False, "empty": False},
            "l10n_latam_identification_type":
            {
                "type": "dict",
                "schema": {
                    "id": {"type": "integer", "coerce": to_int, "nullable": True},
                    "name": {"type": "string"},
                },
            },
            "vat" : {"type": "string", "required": True, "empty": False},
            "street": {"type": "string", "required": False, "empty": False},
            "street2": {"type": "string", "nullable": False},
            "zip": {"type": "string", "required": False, "empty": False},
            "city": {"type": "string", "required": False, "empty": False},
            "phone": {"type": "string", "nullable": True, "empty": False},
            "state": {
                "type": "dict",
                "schema": {
                    "id": {"type": "integer", "coerce": to_int, "nullable": True},
                    "name": {"type": "string"},
                },
            },
            "country": {
                "type": "dict",
                "schema": {
                    "id": {
                        "type": "integer",
                        "coerce": to_int,
                        "required": True,
                        "nullable": False,
                    },
                    "name": {"type": "string"},
                },
            },
            "is_company": {"coerce": to_bool, "type": "boolean"},
            "category_id" : {"type": "string", "required": False, "empty": False},
            "parent_id" : {"type": "string", "required": False, "empty": False},
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

    def _to_json(self, partner):
        res = {
            "id": partner.id,
            "vat": partner.vat,
            "name": partner.name,
            "street": partner.street,
            "street2": partner.street2 or "",
            #"zip": partner.zip,
            "city": partner.city,
            "phone": partner.city,
        }
        if partner.l10n_latam_identification_type_id:
            res["l10n_latam_identification_type"] = {
                "id": partner.l10n_latam_identification_type_id.l10n_pe_vat_code,
                "name": partner.l10n_latam_identification_type_id.name,
            }
        if partner.country_id:
            res["country"] = {
                "id": partner.country_id.id,
                "name": partner.country_id.name,
            }
        if partner.state_id:
            res["state"] = {"id": partner.state_id.id, "name": partner.state_id.name}
        return res
