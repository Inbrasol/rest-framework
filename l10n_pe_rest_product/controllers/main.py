# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.base_rest.controllers import main


class ProductRestPublicApiController(main.RestController):
    _root_path = "/product_rest_api/public/"
    _collection_name = "l10n_pe.product.rest.public.services"
    _default_auth = "public"


class ProductRestPrivateApiController(main.RestController):
    _root_path = "/product_rest_api/private/"
    _collection_name = "l10n_pe.product.rest.private.services"
    _default_auth = "user"

"""
class BaseRestDemoNewApiController(main.RestController):
    _root_path = "/base_rest_demo_api/new_api/"
    _collection_name = "base.rest.demo.new_api.services"
    _default_auth = "public"


class BaseRestDemoJwtApiController(main.RestController):
    # JWT Demo Controller, to be used with auth_jwt_demo
    # https://github.com/OCA/server-auth/tree/15.0/auth_jwt_demo
    _root_path = "/base_rest_demo_api/jwt/"
    _collection_name = "base.rest.demo.jwt.services"
    _default_auth = "jwt_demo_keycloak"
    _component_context_provider = "auth_jwt_component_context_provider"
    _default_cors = "*"
"""