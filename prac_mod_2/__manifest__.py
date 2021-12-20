# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "DOQ Intermedio - Módulo 2",
    "summary": "Práctica módulo 2 del Sistema DOQ Intermedio",
    "version": "14.0.1.0.0",
    "category": "Sistema DOQ",
    "website": "https://www.qubiq.es",
    "author": "QubiQ",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ['sale', 'stock', 'rating'],
    "data": [
        'template/mail.xml',
        'views/product_pricelist.xml',
        'views/stock_picking.xml',
        ],
}
