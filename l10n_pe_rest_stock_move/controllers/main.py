# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.base_rest.controllers import main


class BaseRestDemoPublicApiController(main.RestController):
    _root_path = "/stock_rest_api/public/"
    _collection_name = "l10n_pe.stock.rest.public.services"
    _default_auth = "public"


class BaseRestDemoPrivateApiController(main.RestController):
    _root_path = "/stock_rest_api/private/"
    _collection_name = "l10n_pe.stock.rest.private.services"
    _default_auth = "user"