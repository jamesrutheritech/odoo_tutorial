# -*- coding: utf-8 -*-
{
    "name": "Real Estate",
    "version": "1.0",
    "author": "James Ruther",
    "category": "Sales",
    "sequence": 10,
    "summary": "Real Estate property listing and management",
    "description": """
Real Estate property listing and management.
    """,
    "depends": [
        "base",
    ],
    "data": [
        # 1. SECURITY (Access rights must be loaded first)
        "security/estate_security.xml",  # Make sure this is FIRST
        "security/ir.model.access.csv",
        
        # 2. DATA (Records needed for configuration/defaults)
        "data/estate_property_type_data.xml",
        "data/estate_property_offer_actions.xml",
        
        # 3. VIEWS/ACTIONS (Window actions and view definitions)
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",
        
        # 4. MENUS (Menu items must be loaded after the actions they call)
        "views/estate_menus.xml",
    ],
    "demo": [
        "demo/estate_property_demo.xml",
    ],
    "application": True,
    "installable": True,
    "license": "LGPL-3",
}