# -*- coding: utf-8 -*-

{
    "name": "Real Estate",
    "version": "1.0",
    "author": "James Ruther",
    "category": "Sales",
    "depends": [
        "base",
    ],
    "data": [
        # 1. SECURITY (CSV MUST be loaded first for basic access)
        "security/ir.model.access.csv",

        # 2. MASTER DATA (Records needed by other files/views)
        "data/estate_property_type_data.xml",  

        # 3. VIEWS/ACTIONS
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",

        # 4. SECURITY (Record Rules, relies on views/models being loaded)
        "security/estate_security.xml",

        # 5. MENUS (Usually loaded last as it depends on all actions/views)
        "views/estate_menus.xml",
    ],
    "demo": [
        "demo/estate_property_demo.xml",
    ],
    "application": True,
    "installable": True,
    "license": "LGPL-3",
}