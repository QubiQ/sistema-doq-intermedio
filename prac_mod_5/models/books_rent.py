from odoo import api, fields, models
from odoo.exceptions import ValidationError



class BooksRent(models.Model):
    _name = 'books.rent'
    # 3º Historia de usuario
    partner_id = fields.Many2one(comodel_name="res.partner",
                                 domain="[('is_library_partner', '=', True)]")
    library_partner_code = fields.Char(
        string='Library Partner Code',
        related="partner_id.library_partner_code")
    book_id = fields.Many2one(comodel_name='books.book', string='Book')
    state = fields.Selection(
        string='State',
        selection=[('loan', 'On Loan'), ('returned', 'Returned')],
        default="loan",
        )
    
    loan_date = fields.Datetime(string="Loan Date", default=fields.Datetime.now())
    return_date = fields.Datetime(string="Returned Date")
    
    #Módulo 3 Wizards - Apartado 2
    active = fields.Boolean(default=True)

    @api.constrains('book_id')
    def check_book_type(self):
        for rec in self:
            if rec.book_id and rec.book_id.book_type != 'fisico':
                raise ValidationError("Only physical books can be borrowed")

    # 4º Historia de Usuario
    def return_book(self):
        for rec in self:
            rec.write({'return_date': fields.Datetime.now(),
                       'state': 'returned'})
            
    # 5º Historia de Usuario
    @api.model
    def create(self, vals):
        if 'book_id' in vals:
            book_id = self.env['books.book'].browse(vals.get('book_id'))
            if book_id.qty_available <= 0:
                raise ValidationError("You don't enough quantity to borrow this book")
        return super().create(vals)

    #Módulo 3 wizards - Apartado 1
    def launch_rate_wizard(self):
        return {
            "name":"Rate user",
            "view_mode":"form",
            "res_model":"rate.wizard",
            "target":"new",
            "type":"ir.actions.act_window"
        }
    
    def launch_print_wizard(self):
        return {
            "name":"Print report",
            "view_mode":"form",
            "res_model":"print.wizard",
            "target":"new",
            "type":"ir.actions.act_window"
        }
