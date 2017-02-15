# -*- coding: utf-8 -*-
{
    'name': "seance",

    'summary': "Séance lié a un cours",

    'description': "Les séances d'un cours",

    'author': "Michel R.",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Cours',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
        'views/seance.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}