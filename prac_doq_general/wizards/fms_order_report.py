from odoo import api, models, fields
from odoo.exceptions import UserError

class FmsOrderReport(models.TransientModel):
    _name = 'fms.order.report'
    _description = 'Fms ORder Report'

    start_date = fields.Date(required=True)
    end_date = fields.Date(default=fields.Date.context_today)

    def print_report(self):
        domain = [('scheduled_date_start', '>=', self.start_date)]
        if self.end_date:
            domain.append(('scheduled_date_start', '<=', self.end_date))
        orders = self.env['fsm.order'].search(domain)
        if not orders:
            raise UserError("There aren't Fields Orders for that dates")
        
        return self.env.ref('prac_doq_general.action_report_fms_order').\
            report_action(orders)