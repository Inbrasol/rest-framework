# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo.addons.base_rest.components.service import to_bool, to_int
from odoo.addons.component.core import Component
from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_datamodel.restapi import Datamodel
from odoo import _
from odoo.exceptions import (
    AccessDenied,
    AccessError,
    MissingError,
    UserError,
    ValidationError,
)

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
    _log_calls_in_db = True
    def get(self, _id):
        """
        Get partner's informations
        """
        return self._to_json(self._get(_id))

    @restapi.method(
        [(["/",], "GET")],
        input_param=Datamodel("l10n_pe.partner.search.param"),
        output_param=Datamodel("l10n_pe.partner.info"),
        auth="public",
    )
    def get(self,partner_input):
        try:
            partner = self._get_by_document_type(partner_input.l10n_latam_identification_type_id,partner_input.vat)
            PartnerInfo = self.env.datamodels["l10n_pe.partner.info"]
            partner_info = PartnerInfo(partial=True)
            partner_info.id = partner.id
            partner_info.name = partner.name
            partner_info.street = partner.street
            partner_info.street2 = partner.street2
            partner_info.zip_code = partner.zip
            partner_info.city = partner.city
            partner_info.phone = partner.phone
            if partner.country_id:
                partner_info.country = self.env.datamodels["country.info"](
                    id=partner.country_id.id, name=partner.country_id.name
                )
            if partner.state_id:
                partner_info.state = self.env.datamodels["state.info"](
                    id=partner.state_id.id, name=partner.state_id.name
                )
            partner_info.is_company = partner.is_company
            return partner_info
        except:
            raise ValidationError(_("ValidationError message"))

            
    # pylint:disable=method-required-super
    def create(self, **params):
        if params.get("vat"):
            print(params)
            identification_type = self._get_l10n_latam_identification(params.get("l10n_latam_identification_type").get("l10n_pe_vat_code"))
            print("------------identification_type-----------")
            print(identification_type)
            partner_search = self._get_by_document_type(params.get("l10n_latam_identification_type").get("l10n_pe_vat_code"),params.get("vat"))
            if partner_search:
                return self._to_json(partner_search)
            else :
                prepare_params_doc_type = self._prepare_document_type_params(params,identification_type)
                print("-----prepare_params_doc_type---------")
                print(prepare_params_doc_type)
                print("------------------create---------------------------")
                create_params = self._prepare_params(prepare_params_doc_type)
                print(create_params)
                if params.get("parent_id") and params.get("company_type")=="person":
                    print("dataaaaaaaaaaaaaaaa")
                    parent_search = self._get_by_document_type(params.get("parent_id").get("l10n_pe_vat_code"),params.get("parent_id").get("vat"))
                    print("dataaaaaaaaaaaaaaaa3333")
                    create_params.pop("parent_id")
                    print(create_params)
                    create_params["parent_id"] = parent_search.id
                    print("----parent-id")
                    print(create_params)
                    partner = self.env["res.partner"].create(self._prepare_params(create_params))
                else:
                    partner = self.env["res.partner"].create(self._prepare_params(create_params))
                return self._to_json(partner, "new")
 
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
        identification_type = self._get_l10n_latam_identification(params.get("l10n_latam_identification_type").get("l10n_pe_vat_code"))
        partner = self._get_by_document_type(params.get("l10n_latam_identification_type").get("l10n_pe_vat_code"),params.get("vat"))
        prepare_params_doc_type = self._prepare_document_type_params(params,identification_type)

        if identification_type.l10n_pe_vat_code == "1":
            prepare_params_doc_type.pop("name", None)
            prepare_params_doc_type.pop("vat", None)
            prepare_params_doc_type.pop("l10n_latam_identification_type_id", None)
        elif identification_type.l10n_pe_vat_code == "6":
            prepare_params_doc_type.pop("name", None)
            prepare_params_doc_type.pop("vat", None)
            prepare_params_doc_type.pop("l10n_latam_identification_type_id", None)
            prepare_params_doc_type.pop("street", None)
            prepare_params_doc_type.pop("state", None)

        partner.write(self._prepare_params(prepare_params_doc_type))

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

    def _prepare_params(self, params):
        for key in ["country", "state"]:
            if key in params:
                val = params.pop(key)
                if val.get("id"):
                    params["%s_id" % key] = val["id"]
        
        

        return params

    def _prepare_document_type_params(self, params,l10n_latam_identification_type):
        for key in ["l10n_latam_identification_type"]:
            if key in params:
                print(l10n_latam_identification_type)
                val = params.pop(key)
                print("------val-----------")
                print(val)
                if val.get("l10n_pe_vat_code"):
                    params["%s_id" % key] = l10n_latam_identification_type["id"]
        print(params)
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
            "company_type":{"type": "string", "required": True, "empty": False},
            "l10n_latam_identification_type":
            {
                "type": "dict",
                "schema": {
                    "id": {"type": "integer", "coerce": to_int, "nullable": True},
                    "name": {"type": "string"},
                    "l10n_pe_vat_code":  {"type": "string"}
                },
            },
            "parent_id":
            {
                "type": "dict",
                "schema": {
                    "l10n_pe_vat_code":  {"type": "string"},
                    "vat":  {"type": "string"},
                },
            },
            "vat" : {"type": "string", "required": True, "empty": False},
            "street": {"type": "string", "required": False, "empty": True},
            "email": {"type": "string", "required": False, "empty": True},
            "street2": {"type": "string", "nullable": True},
            "zip": {"type": "string", "required": False, "empty": True},
            "city": {"type": "string", "required": False, "empty": True},
            "phone": {"type": "string", "nullable": False, "empty": True},
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
                        "required": False,
                        "nullable": True,
                    },
                    "name": {"type": "string"},
                },
            },
            "is_company": {"coerce": to_bool, "type": "boolean","empty": True},
            "category_id" : {"type": "string", "required": False, "empty": True},
            "transaction_status" : {"type": "string", "required": False, "empty": True},
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

    def _to_json(self, partner, transaction_status="exists"):
        res = {
            "id": partner.id,
            "company_type": partner.company_type,
            "vat": partner.vat,
            "name": partner.name,
            "street": partner.street or "",
            "street2": partner.street2 or "",
            "zip": partner.zip or "",
            "city": partner.city or "",
            "phone": partner.phone or "",
            "transaction_status": transaction_status,
        }
        if partner.l10n_latam_identification_type_id:
            res["l10n_latam_identification_type"] = {
                "id": partner.l10n_latam_identification_type_id.id,
                "l10n_pe_vat_code": partner.l10n_latam_identification_type_id.l10n_pe_vat_code,
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
