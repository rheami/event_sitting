# -*- coding: utf-8 -*-
from datetime import timedelta
from openerp import models, fields, api, _
from openerp.exceptions import AccessError, Warning

class event_event(models.Model):
    _inherit = 'event.event'
            
    seance_ids = fields.One2many('event.seance', 'event_id', string="Séances", readonly=False)


class event_seance(models.Model):
#    _inherits = {'event.event'}    
    _name = 'event.seance'

    name = fields.Char(string="Title", required=True)
    
    # take the name from event.event_ticket_ids -> name
    #event_ticket_id = fields.Selection(related='event_id.event_ticket_ids')               # KeyError: 'event_ticket_ids'
    
    description = fields.Char()
       
    date_begin_seance = fields.Datetime(string='Date et heure de la séance', required=True)
    
    date_end_seance = fields.Datetime(string="Fin de la scéance", store=True, readonly=True,
        compute='_get_date_end_seance')
            
    # todo ajouter contrainte max = max variable globale
    duration = fields.Float(string='Durée', digits=(2, 2), help="En heures", default=1)
    
    local = fields.Char()
    
    event_id = fields.Many2one( # evenement parent
        'event.event',
        ondelete='cascade',
        string="Event",
       # domain=[('type_id.name','ilike',"Cours")], # a tester
        required=True)
    
    event_date_begin = fields.Datetime(
        string='Date et heure debut',
        related='event_id.date_begin')
     
    event_date_end = fields.Datetime(
        string='Date et heure fin',
        related='event_id.date_end')
     
    @api.constrains('date_begin_seance', 'event_date_begin', 'event_date_end', 'name')
    def _check_date_time(self):
        if self.date_begin_seance < self.event_date_begin :
            raise Warning(_("La date de la séance {} ne peut être avant la date de début de l'évènement.".format(self.name)))
        if self.date_begin_seance > self.event_date_end  :
            raise Warning(_("La date de la séance {} ne peut être après la date de fin de l'évènement.".format(self.name)))


    @api.depends('date_begin_seance', 'duration')
    def _get_date_end_seance(self):
        for r in self:
            if not (r.date_begin_seance and r.duration):
                r.date_end_seance = r.date_begin_seance
                continue

            begin = fields.Datetime.from_string(r.date_begin_seance)
            r.date_end_seance = begin + timedelta(hours=r.duration)
    
    
    
    
    
    
    
    
    
    
  