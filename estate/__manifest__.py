# -*- coding: utf-8 -*-

{
    "name": "Real Estate",
    "version": "1.0",
    "author": "James Ruther",
    "category": "Sales",
    "depends": [
        "base",
        "base_import_module",  # required for importable modules
    ],
    "data": [
        # 1. SECURITY (CSV MUST be loaded first for basic access)
        "security/ir.model.access.csv",

        # 2. MODEL DEFINITIONS (must come before views)
        "models/estate_property.xml",   # ✅ corrected path

        # 3. MASTER DATA (Records needed by other files/views)
        "data/estate_property_type_data.xml",

        # 4. VIEWS/ACTIONS
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",

        # 5. SECURITY (Record Rules, relies on views/models being loaded)
        "security/estate_security.xml",

        # 6. MENUS (Usually loaded last as it depends on all actions/views)
        "views/estate_menus.xml",
    ],
    "demo": [
        "demo/estate_property_demo.xml",
    ],
    "application": True,
    "installable": True,
    "license": "LGPL-3",
}
