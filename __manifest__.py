{
    'name': 'GearGuard',
    'version': '1.0',
    'summary': 'Equipment Maintenance Management',
    'description': """
        GearGuard Module for managing equipment, maintenance teams, and maintenance requests.
    """,
    'author': 'Antigravity',
    'category': 'Operations/Maintenance',
    'depends': ['base', 'mail', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/gearguard_team_views.xml',
        'views/gearguard_equipment_views.xml',
        'views/gearguard_request_views.xml',
        'views/gearguard_menus.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}