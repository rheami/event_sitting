# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import timedelta

from openerp import models, fields, api, _
#from openerp.exceptions import Warning
from .. import exceptions


class EventEvent(models.Model):
    _inherit = 'event.event'

    event_sitting_ids = fields.One2many('event.sitting', 'event_id', string="Sitting", readonly=False)
    event_ref_sitting_ids = fields.One2many('event.sitting', 'event_ref_id', string="Sitting", readonly=False)
    forbid_duplicates_sittings = fields.Boolean()

    # @api.multi
    # @api.constrains("forbid_duplicates_sittings", "event_sitting_ids")
    # def _check_forbid_duplicates_sittings(self):
    #     """Ensure no duplicated sittings are found in the event."""
    #     return self.filtered("forbid_duplicates_sittings").event_sitting_ids._check_forbid_duplicates_sittings()


class Event_event_ticket(models.Model):
    _inherit = 'event.event.ticket'

    sitting_ids = fields.One2many('event.sitting', 'event_ticket_id', string="Sitting", readonly=False)


class Event_sitting(models.Model):
    _name = 'event.sitting'

    name = fields.Char(compute='_get_name', store=True)
    event_ticket_id = fields.Many2one('event.event.ticket', string="Event Ticket", required=True)
    description = fields.Char(required=True)
    sitting_date_begin = fields.Datetime(string='Start of sitting',
                                         default=lambda self: fields.datetime.now().replace(second=0, microsecond=0),
                                         required=True)
    sitting_date_end = fields.Datetime(string="End of sitting", store=True, readonly=True,
                                       compute='_get_sitting_date_end')

    duration = fields.Float(string='Duration', digits=(2, 2), help="In hours", default=1)
    event_id = fields.Many2one(
        'event.event',
        ondelete='cascade',
        required=True,
        domain=[('type', 'like', "Cours")]
    )
    event_ref_id = fields.Many2one(
        'event.event',
        ondelete='cascade',
        required=True,
        domain=[('type', 'like', "Location")]
    )
    event_date_begin = fields.Datetime(string='Start of event', related='event_id.date_begin')
    event_date_end = fields.Datetime(string='End of event', related='event_id.date_end')

    # @api.multi
    # @api.constrains("event_id", "sitting_id")
    # def _check_forbid_duplicates_sittings(self):
    #     """Ensure no duplicated sittings are found in the event."""
    #     for s in self.filtered("event_id.forbid_duplicates_sittings"):
    #         dupes = self.search(s._duplicate_search_domain())
    #         if dupes:
    #             raise exceptions.DuplicatedSittingError(
    #                 s.event_id.display_name,
    #                 ", ".join(d.display_name
    #                           for d in dupes.mapped("sitting_id")),
    #                 sittings=dupes,
    #             )

    @api.multi
    def _duplicate_search_domain(self):
        """What to look for when searching duplicates."""
        return ['|',
                ("sitting_id", "=", self.id),
                #("event_ref_id", "=", self.event_ref_id.id),  # meme local + todo meme plage de temps
                '&', # meme plage de temps :
                ("sitting_date_begin", "<", self.sitting_date_end),
                ("sitting_date_end", ">", self.sitting_date_begin)
        ]

    @api.depends('event_ticket_id', 'description')
    def _get_name(self):
        for r in self:
            r.name = u'%s (%s)' % (r.description, r.event_ticket_id.name)

    @api.constrains('sitting_date_begin', 'event_date_begin', 'event_date_end', 'name')
    def _check_date_time(self):
        if self.sitting_date_begin < self.event_date_begin:
            raise Warning(
                _("The date of the session {} can not be before the start date of the event.".format(self.name)))
        if self.sitting_date_begin > self.event_date_end:
            raise Warning(
                _("The date of the session {} can not be after the end date of the event.".format(self.name)))

    @api.depends('sitting_date_begin')
    def _get_sitting_date_end(self):
        for r in self:
            begin = fields.Datetime.from_string(r.sitting_date_begin).replace(second=0, microsecond=0)
            r.sitting_date_begin = begin

    @api.depends('sitting_date_begin', 'duration')
    def _get_sitting_date_end(self):
        for r in self:
            if not (r.sitting_date_begin and r.duration):
                r.sitting_date_end = r.sitting_date_begin
                continue

            begin = fields.Datetime.from_string(r.sitting_date_begin).replace(second=0, microsecond=0)
            r.sitting_date_end = begin + timedelta(hours=r.duration)

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = [] if args is None else args.copy()
        if not(name == '' and operator == 'ilike'):
            args += ['|', '|',
                     ('name', operator, name),
                     ('description', operator, name),
                     ('event_ticket_id.name', operator, name)
                     ]
        return super(Event_sitting, self)._name_search( name='', args=args, operator='ilike',
                                                        limit=limit, name_get_uid=name_get_uid)
