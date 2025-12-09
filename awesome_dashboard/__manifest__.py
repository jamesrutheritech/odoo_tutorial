{
    'name': 'Awesome Dashboard',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Custom Dashboard',
    'depends': ['web', 'base', 'crm'],
    'data': [
        'views/dashboard_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'awesome_dashboard/static/src/dashboard_action.js',
            'awesome_dashboard/static/src/xml/dashboard_loader.xml',
            'awesome_dashboard/static/src/dashboard/statistics_service.js',
        ],
        'awesome_dashboard.dashboard_assets': [
            'awesome_dashboard/static/src/dashboard/*.js',
            'awesome_dashboard/static/src/xml/dashboard.xml',
            'awesome_dashboard/static/src/dashboard/*.scss',
        ],
    },
    'installable': True,
    'application': True,
}