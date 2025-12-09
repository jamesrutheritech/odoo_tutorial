# -*- coding: utf-8 -*-
{
    'name': "Awesome Kanban",
    'summary': """
        Starting module for "Master the Odoo web framework, chapter 4: Customize a kanban view"
    """,
    'description': """
        Starting module for "Master the Odoo web framework, chapter 4: Customize a kanban view.
    """,
    'version': '0.1',
    'application': True,
    'category': 'Tutorials',
    'installable': True,
    'depends': ['web', 'crm'],
    'data': [
        'views/views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'awesome_kanban/static/src/js/customer_list.js',
            'awesome_kanban/static/src/xml/customer_list.xml',
            'awesome_kanban/static/src/js/awesome_kanban_controller.js',
            'awesome_kanban/static/src/js/awesome_kanban_renderer.js',
            'awesome_kanban/static/src/js/awesome_kanban_view.js',
            'awesome_kanban/static/src/xml/awesome_kanban_controller.xml',
            'awesome_kanban/static/src/scss/customer_list.scss',
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'AGPL-3'
}