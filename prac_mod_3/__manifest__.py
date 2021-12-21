# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Práctica Final 3",
    "summary": "Práctica Final 3 Sistema DOQ Base",
    "version": "14.0.1.0.0",
    "category": "Sistema DOQ",
    "website": "https://www.qubiq.es",
    "author": "QubiQ",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [],
    "data": ['security/ir.model.access.csv',
             'data/menu.xml',
             'wizards/rate_wizard.xml',
             'wizards/print_wizard.xml',
             'wizards/sign_up.xml',
             'wizards/rent_book_wizard.xml',
             'wizards/return_book_wizard.xml',
             'views/res_partner.xml',
             'views/books_book.xml',
             'views/books_author.xml',
             'views/report_books.xml',
             'views/books_rent.xml',
             'views/reports.xml',
             'views/books_genre.xml'],
}
