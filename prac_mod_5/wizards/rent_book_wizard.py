from odoo import fields, models
from odoo.exceptions import ValidationError

class RentBook(models.TransientModel):
    _name = 'rent.book.wizard'
    _description = 'New Description'

    book_id = fields.Many2one(comodel_name="books.book", string="Book", required=True)

    def rent_book(self):
        
        #primero hacemos check por si hay que bloquear (ya tiene 2 rents en loan)
        if len(self.env["books.rent"].search([('partner_id','=', self._context["active_id"]), ('state', '=', 'loan')])) == 2:
            self.env["res.partner"].browse(self._context["active_id"]).write({"can_rent":False})
            raise ValidationError("This user has passed the rent limit!")
        
        #Procedemos con el proceso de rent
        partner_id = self._context["active_id"]
        partner_code = self.env["res.partner"].browse(partner_id).library_partner_code
        
        if self.env["res.partner"].browse(partner_id).can_rent:
            
            self.env["books.rent"].create({
                "partner_id":partner_id,
                "book_id":self.book_id.id,
                "state":"loan",
                "loan_date":fields.datetime.now(),
                "library_partner_code":partner_code
                })