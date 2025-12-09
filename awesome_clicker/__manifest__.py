# -*- coding: utf-8 -*-
{
    'name': "Awesome Clicker",
    'summary': """
        Starting module for "Master the Odoo web framework, chapter 1: Build a Clicker game"
    """,
    'description': """
        Starting module for "Master the Odoo web framework, chapter 1: Build a Clicker game"
    """,
    'author': "Odoo",
    'website': "https://www.odoo.com/",
    'category': 'Tutorials',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['base', 'web'],
    'data': [],
    'assets': {
        'web.assets_backend': [
            # Styles - load first
            'awesome_clicker/static/src/clicker_styles.scss',
            
            # Utilities - load first
            'awesome_clicker/static/src/utils/utils.js',
            'awesome_clicker/static/src/utils/click_rewards.js',
            
            # Models - load before services
            'awesome_clicker/static/src/models/clicker_model.js',
            
            # Services - load before components that use them
            'awesome_clicker/static/src/services/clicker_service.js',
            
            # Commands
            'awesome_clicker/static/src/commands/clicker_commands.js',
            
            # Patches
            'awesome_clicker/static/src/patches/form_controller_patch.js',
            
            # Components - JS files first, then XML
            'awesome_clicker/static/src/components/click_value.js',
            'awesome_clicker/static/src/components/click_value.xml',
            'awesome_clicker/static/src/components/clicker_systray_item.js',
            'awesome_clicker/static/src/components/clicker_systray_item.xml',
            'awesome_clicker/static/src/components/client_action.js',
            'awesome_clicker/static/src/components/client_action.xml',
        ],
    },
    'license': 'AGPL-3'
}