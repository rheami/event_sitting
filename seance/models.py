# -*- coding: utf-8 -*-

from openerp import models, fields, api

# import event

class seance(models.Model):
    _name = 'seance.seance'
    
    # take the name from event.ticket_ids -> name
    name = fields.Char(string="Title", required=True)
    
    description = fields.Text()
    
    seance_date = fields.Date()
    
    duration = fields.Float(digits=(2, 2), help="Duration in hours")
    
    local = fields.Text()
    
    event_id = fields.Many2one( # evenement principal
        'seance.seance',
        ondelete='cascade',
        string="Event",
        required=True)
    
    
    
    # event # evenement pour affichage dans le calendrier
    
# @api.constraints('seance_date', 'start_date', 'end_date')
# def _check_date_time(self):
#     if self.seance_date > self.end_date or elf.seance_date < self.star_date :
#         raise ValidationError(_('La date n est pas valide.'))

# create sub event here
# @api.model
# def create(self, values):