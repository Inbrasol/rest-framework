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
