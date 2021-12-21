from odoo import api, fields, models
# Importamos libreria para mostrar errores
from odoo.exceptions import UserError


class BooksBook(models.Model):
    _name = 'books.book'
    _description = 'Books'

    name = fields.Char(required=True)
    price = fields.Float()
    # ISBN
    barcode = fields.Char(string='ISBN')
    edition = fields.Integer()
    book_type = fields.Selection(
        selection=[('fisico', 'Fisico'), ('digital', 'Digital')])
    website = fields.Char()
    date = fields.Date(string='Purchase Date')
    author_id = fields.Many2one(comodel_name='books.author')
    genre_ids = fields.Many2many(comodel_name='books.genre',
                                 string="Genres")

    dealer_line_ids = fields.One2many(
        comodel_name='books.dealer.line',
        inverse_name='book_id', string='Dealers')
    editorial_line_ids = fields.One2many(
        comodel_name='books.editorial.line',
        inverse_name='book_id', string='Editorial')
    rent_line_ids = fields.One2many(
        comodel_name="books.rent",
        inverse_name="book_id",
        string="Loans"
    )
    
    rent = fields.One2many(comodel_name="rent.book.wizard", inverse_name="book_id", invisible="1")
    #return_book = fields.One2many(comodel_name="return.book.wizard", inverse_name="book_id", invisible="1")
    
    # 5º Historia de usuario
    qty_total = fields.Integer(string='Quantity on Hand')
    qty_borrowed = fields.Integer(string='Quantity Borrowed',
                                  compute="_compute_qty")
    qty_available = fields.Integer(string="Quantity Available",
                                   compute="_compute_qty")
    
    @api.depends('qty_total', 'rent_line_ids')
    def _compute_qty(self):
        for rec in self:
            rec.qty_borrowed = len(self.rent_line_ids.filtered(
                lambda x: x.state == 'loan'))
            # Es lo mimsmo que:
            # rec.qty_borrowed = 0
            # for line in rec.rent_line_ids:
            #     if line.state == 'loan':
            #         rec.qty_borrowed += 1
            rec.qty_available = rec.qty_total - rec.qty_borrowed
            
    
    
