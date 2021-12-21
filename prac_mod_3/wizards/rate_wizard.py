from odoo import fields, models


class RateWizard(models.TransientModel):
    _name = 'rate.wizard'
    _description = 'Wizard that controls the user rate system.'

    book_state = fields.Selection(selection = [('5', "Excellent"), ('3', "Good"), ('-3', "Bad"), ('-5' ,"Very Bad")])
    
    #rate suma valoracion y archiva el rent
    def rate_user(self):
        
        #guardamos el id de la entrada de books.rent usando el context
        rent_id = self._context["active_id"]
        
        #obtenemos del context el id del partner activo
        partner_id = self.env["books.rent"].browse(rent_id).partner_id
        
        #creamos entrada en rate.partner
        self.env["rate.partner"].create({'partner_id':partner_id.id, 'rent_rate':self.book_state})
        
        #para archivar el rent ponemos la variable active en False
        self.env["books.rent"].browse(rent_id).active = False
