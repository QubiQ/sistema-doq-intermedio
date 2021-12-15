from odoo import api, fields, models
import time


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    total_heavy_units = fields.Integer(compute="_compute_total_heavy_units",
                                       store=True)

    partner_bank_id = fields.Many2one(
        comodel_name='res.partner.bank', string='Bank')

    @api.onchange('partner_id')
    def onchange_bank_partner_id(self):
        partner_id = self.partner_id.id if self.partner_id else False
        return {'domain':
                {'partner_bank_id': [('partner_id', '=', partner_id)]}}

    @api.depends('order_line.product_id', 'order_line.product_id.weight',
                 'order_line.product_uom_qty')
    def _compute_total_heavy_units(self):
        # NEW WAY EXC TIME: 0.007364s
        for rec in self:
            rec.total_heavy_units = sum(rec.order_line.filtered(
                lambda x: x.product_id and x.product_id.weight > 3).
                    mapped('product_uom_qty'))

        # OLD WAY EXC TIME: 0.007224s
        # for rec in self:
        #     qty = 0
        #     for line in rec.order_line:
        #         if line.product_id and line.product_id.weight > 3:
        #             qty += line.product_uom_qty
        #     rec.total_heavy_units = qty
