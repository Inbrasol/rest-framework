# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.base_rest.controllers import main

class PartnerRestPublicApiController(main.RestController):
    _root_path = "/partner_rest_api/public/"
    _collection_name = "l10n_pe.partner.rest.public.services"
    _default_auth = "public"


class PartnerRestPrivateApiController(main.RestController):
    _root_path = "/partner_rest_api/private/"
    _collection_name = "l10n_pe.partner.rest.private.services"
    _default_auth = "user"


"""
class PartnerRestJwtApiController(main.RestController):
    # JWT Demo Controller, to be used with auth_jwt_demo
    # https://github.com/OCA/server-auth/tree/15.0/auth_jwt_demo
    _root_path = "/base_rest_demo_api/jwt/"
    _collection_name = "base.rest.demo.jwt.services"
    _default_auth = "jwt_demo_keycloak"
    _component_context_provider = "auth_jwt_component_context_provider"
    _default_cors = "*"
"""