# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "DOQ Intermedio - Pŕactica General",
    "summary": "Práctica general del Sistema DOQ Intermedio",
    "version": "14.0.1.0.0",
    "category": "Sistema DOQ",
    "website": "https://www.qubiq.es",
    "author": "QubiQ",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ['fieldservice', 'maintenance', 'product'],
    "data": [
        'security/ir.model.access.csv',
        'views/maintenance_equipment.xml',
        'views/fsm_order.xml',
        'views/fsm_equipment_report.xml',
        'wizards/fms_order_report.xml',
        'data/actions.xml',
        'data/mail_template.xml',
        ],
}
