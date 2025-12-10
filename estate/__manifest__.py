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
        # 1. SECURITY - Must be loaded FIRST
        "security/ir.model.access.csv",
        
        # 2. DATA
        "data/estate_property_type_data.xml",
        
        # 3. VIEWS
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_menus.xml",
    ],
    "demo": [
        "demo/estate_property_demo.xml",
    ],
    "application": True,
    "installable": True,
    "license": "LGPL-3",
}