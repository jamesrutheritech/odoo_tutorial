# -*- coding: utf-8 -*-

{
    "name": "Real Estate",
    "version": "1.0",
    "category": "Sales",
    "depends": [
        "base",
    ],
    "data": [
        "security/estate_security.xml",
        "security/ir.model.access.csv",

        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",

        "views/estate_menus.xml",

        "data/estate_property_type_data.xml",
    ],
    "demo": [
        "demo/estate_property_demo.xml",
    ],
    "application": True,
    "installable": True,
    "license": "LGPL-3",
}
