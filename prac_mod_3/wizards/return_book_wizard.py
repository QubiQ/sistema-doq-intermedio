from odoo import fields, models


class ReturnBookWizard(models.TransientModel):
    _name = 'return.book.wizard'
    _description = 'Wizard that controls the returning process.'

    def book_doma(self):

        activ = self._context.get("active_id")
        partner_rents = self.env["books.rent"].search([('partner_id', '=', activ), ('state', '=', 'loan')])
        return [('id', 'in', partner_rents.book_id.ids)]

    book_id = fields.Many2one(comodel_name="books.book", string="Rent", domain=book_doma, required=True)
    
    def return_book(self):

        rent = self.env["books.rent"].search([('partner_id','=', self._context["active_id"]), ('state','=', 'loan'), ('book_id', '=', self.book_id.id)])
        rent.write({'state':'returned', 'return_date':fields.datetime.now()})
