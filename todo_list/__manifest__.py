{
    'name': 'To-Do List',
    'version': '1.0',
    'license': 'LGPL-3',
    'author': 'James Ruther',
    'summary': 'A list of tasks to manage daily work.',
    'category': 'Productivity',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/todo_task_views.xml',
    ],
    'installable': True,
    'application': True,
}
