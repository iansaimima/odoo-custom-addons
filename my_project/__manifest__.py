{
    'name': 'My Project',
    'version': '1.0',
    'summary': 'Custom Inherit Project',
    'description': 'Module to manage tasks in Odoo 17',
    'author': 'BPP',
    'category': 'Library',
    'depends' : [
        'mail', 'project'
    ],
    'data' : [
        "views/my_project_view.xml",
        "views/my_project_task_view.xml"
    ]
}
