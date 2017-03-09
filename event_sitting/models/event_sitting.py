# -*- coding: utf-8 -*-
from datetime import timedelta
from openerp import models, fields, api, _
from openerp.exceptions import AccessError, Warning


class event_event(models.Model):
    _inherit = 'event.event'

    sitting_ids = fields.One2many('event.sitting', 'event_id', string="Séances", readonly=False)


class event_event_ticket(models.Model):
    _inherit = 'event.event.ticket'

    sitting_ids = fields.One2many('event.sitting', 'event_ticket_id', string="Séances", readonly=False)


class event_sitting(models.Model):
    _name = 'event.sitting'

    name = fields.Char(string="Title", required=True)
    # take the name from event.event_ticket_ids -> select -> product -> name
    event_ticket_id = fields.Many2one('event.event.ticket', string="Event Ticket")

    description = fields.Char()
    date_begin_sitting = fields.Datetime(string='Date et heure de la séance', required=True)
    date_end_sitting = fields.Datetime(string="Fin de la scéance", store=True, readonly=True,
                                       compute='_get_date_end_sitting')
    # todo ajouter contrainte max = max variable globale
    duration = fields.Float(string='Durée', digits=(2, 2), help="En heures", default=1)
    local = fields.Char()
    event_id = fields.Many2one('event.event', string="Event", ondelete='cascade',
                               required=True)  # domain=[('type_id.name','ilike',"Cours")], # a tester
    event_date_begin = fields.Datetime(string='Date et heure debut', related='event_id.date_begin')
    event_date_end = fields.Datetime(string='Date et heure fin', related='event_id.date_end')

    @api.constrains('date_begin_sitting', 'event_date_begin', 'event_date_end', 'name')
    def _check_date_time(self):
        if self.date_begin_sitting < self.event_date_begin:
            raise Warning(
                _("La date de la séance {} ne peut être avant la date de début de l'évènement.".format(self.name)))
        if self.date_begin_sitting > self.event_date_end:
            raise Warning(
                _("La date de la séance {} ne peut être après la date de fin de l'évènement.".format(self.name)))

    @api.depends('date_begin_sitting', 'duration')
    def _get_date_end_sitting(self):
        for r in self:
            if not (r.date_begin_sitting and r.duration):
                r.date_end_sitting = r.date_begin_sitting
                continue

            begin = fields.Datetime.from_string(r.date_begin_sitting)
            r.date_end_sitting = begin + timedelta(hours=r.duration)