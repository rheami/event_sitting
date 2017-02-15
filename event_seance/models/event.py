# -*- coding: utf-8 -*-

from openerp import models, fields, api


class EventEvent(models.Model):
    _name = 'event.event'
    _inherit = [_name]

    seance_ids = fields.One2many(
        'seance.seance',
        'event_id',
        string="Séances")