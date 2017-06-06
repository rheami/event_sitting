# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Sitting in events',
    'summary': 'Add sitting to event',
    'version': '8.0.1.0.0',
    'category': 'Events',
    'website': '',
    'author': 'Michel Rheault',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'event',
        'event_sale'
    ],
    'data': [
        'views/event_event_view.xml',
        'views/event_sitting_view.xml',
        'report/event_sitting_report.xml'
    ],
}
