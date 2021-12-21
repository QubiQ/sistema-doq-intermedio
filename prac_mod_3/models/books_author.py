from odoo import fields, models


class ModuleAuth(models.Model):
    _name = 'books.author'
    _description = 'autores'

    name = fields.Char(required=True)
    books_ids = fields.One2many(
        comodel_name='books.book', inverse_name='author_id')
    genre_ids = fields.Many2many(comodel_name='books.genre', string="Genres")
