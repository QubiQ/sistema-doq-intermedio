# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "DOQ Intermedio - Módulo 1",
    "summary": "Práctica módulo 1 del Sistema DOQ Intermedio",
    "version": "14.0.1.0.0",
    "category": "Sistema DOQ",
    "website": "https://www.qubiq.es",
    "author": "QubiQ",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ['sale', 'stock'],
    "data": [
        'views/sale_order.xml',
        'views/res_partner.xml'
        ],
}
