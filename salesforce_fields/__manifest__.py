# Copyright 2016 Antiun Ingenieria S.L. - Antonio Espinosa
# Copyright 2017 Tecnativa - Vicent Cubells
# Copyright 2020 Tecnativa - João Marques
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Rest-Salesforce Fields",
    "summary": "Add Salesforce fields to Odoo",
    "version": "17.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["base", "account", "sale", "stock", "iws_crm_purchase"],
    "data": [
        "views/res_company_views.xml",
        "views/res_user_views.xml",
        "views/res_currency_views.xml",
        "views/res_partner_views.xml",
        "views/sale_order_views.xml",
        "views/crm_lead_views.xml",
        "views/product_template_views.xml",
        "views/account_move_views.xml",
    ],
    "application": False,
    "installable": True,
    'post_init_hook': 'post_init_hook',
}
