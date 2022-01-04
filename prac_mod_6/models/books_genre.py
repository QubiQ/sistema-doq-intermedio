from odoo import fields, models


class BooksGenre(models.Model):
    _name = 'books.genre'
    _description = 'Books Genre'

    name = fields.Char()
