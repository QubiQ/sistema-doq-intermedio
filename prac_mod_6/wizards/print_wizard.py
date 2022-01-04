from odoo import fields, models
from odoo.exceptions import ValidationError

class PrintWizard(models.TransientModel):
    _name = 'print.wizard'
    _description = 'Wizard that we will use to control which rent entries we have to be printed.'

    def dynamic_domain(self):
        return [('id', 'in', self.env['books.rent'].search([]).partner_id.ids)]

    partner_id = fields.Many2one(comodel_name="res.partner", string="User", required=True, domain = dynamic_domain)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    
    def print_report(self):
        to_print = self.env["books.rent"].search([('partner_id','=',self.partner_id.id), ('loan_date','>=', self.start_date), ('loan_date', '<=', self.end_date) ])
        if len(to_print)<1:
            raise ValidationError("No rents were made between these two dates!")
        else:
            return self.env.ref("practica_final_3.wizard_print").report_action(to_print)

    #Práctica módulo 5 - Vistas
    def print_sql_report(self):
        all_entries = self.env["report.sql"].search([])
        return self.env.ref("practica_final_3.report_sql").report_action(all_entries)