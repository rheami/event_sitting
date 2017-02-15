# -*- coding: utf-8 -*-
from openerp import http

# class seance(http.Controller):
#     @http.route('/seance/seance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/seance/seance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('seance.listing', {
#             'root': '/seance/seance',
#             'objects': http.request.env['seance.seance'].search([]),
#         })

#     @http.route('/seance/seance/objects/<model("seance.seance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('seance.object', {
#             'object': obj
#         })