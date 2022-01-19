from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def get_pending_sale_order(self, date=fields.Date.today()):
        sales = self.env['sale.order'].search(
            [('date_order', '>=', date),
             ('picking_ids.state', 'not in', ['done', 'cancel'])])
        return sales.mapped('name')
