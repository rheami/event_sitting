# -*- coding: utf-8 -*-
from datetime import timedelta

from openerp import models, fields, api, _
from openerp.exceptions import Warning


class event_event(models.Model):
    _inherit = 'event.event'

    event_sitting_ids = fields.One2many('event.sitting', 'event_id', string="Sitting", readonly=False)
    room_sitting_ids = fields.One2many('event.sitting', 'room_id', string="Sitting", readonly=False)
    sitting_ids = event_sitting_ids

class event_event_ticket(models.Model):
    _inherit = 'event.event.ticket'

    sitting_ids = fields.One2many('event.sitting', 'event_ticket_id', string="Sitting", readonly=False)

class event_sitting(models.Model):
    _name = 'event.sitting'

    name = fields.Char(string="Title", related = 'event_ticket_id.name')
    event_ticket_id = fields.Many2one('event.event.ticket', string="Event Ticket", required=True)
    description = fields.Char()
    sitting_date_begin = fields.Datetime(string='Start of sitting', required=True)
    sitting_date_end = fields.Datetime(string="End of sitting", store=True, readonly=True,
                                       compute='_get_date_end_sitting')
    duration = fields.Float(string='Duration', digits=(2, 2), help="In hours", default=1)
    event_id = fields.Many2one('event.event', string="Event", ondelete='cascade', required=True, domain=[('type', 'like', "Cours")])
    room_id = fields.Many2one('event.event', string="Room", ondelete='cascade', required=True,
                              domain=[('type', 'like', "Location")])
    event_date_begin = fields.Datetime(string='Start of event', related='event_id.date_begin')
    event_date_end = fields.Datetime(string='End of event', related='event_id.date_end')

    @api.constrains('sitting_date_begin', 'event_date_begin', 'event_date_end', 'name')  # todo check minutes
    def _check_date_time(self):
        if self.sitting_date_begin < self.event_date_begin:
            raise Warning(
                _("The date of the session {} can not be before the start date of the event.".format(self.name)))
        if self.sitting_date_begin > self.event_date_end:
            raise Warning(
                _("The date of the session {} can not be after the end date of the event.".format(self.name)))

    @api.depends('sitting_date_begin', 'duration')
    def _get_date_end_sitting(self):
        for r in self:
            if not (r.sitting_date_begin and r.duration):
                r.sitting_date_end = r.sitting_date_begin
                continue

            begin = fields.Datetime.from_string(r.sitting_date_begin)
            r.sitting_date_end = begin + timedelta(hours=r.duration)
