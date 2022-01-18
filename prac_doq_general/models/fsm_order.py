from odoo import api, fields, models
from odoo.exceptions import ValidationError


class FsmOrder(models.Model):
    _inherit = 'fsm.order'

    equipment_line_ids = fields.One2many(
        comodel_name='fsm.equimnet.line',
        inverse_name='fsm_order_id')

    total_weight = fields.Float(compute="_compute_total_weight", store=True)
    weight_name = fields.Char(compute="_compute_weight_name")

    def _compute_weight_name(self):
        for rec in self:
            rec.weight_name = self.env['product.template'].\
                _get_weight_uom_name_from_ir_config_parameter()

    @api.depends('equipment_line_ids.equipment_id')
    def _compute_total_weight(self):
        for rec in self:
            rec.total_weight = sum(rec.equipment_line_ids.mapped(
                'equipment_id.weight'))
    @api.model
    def _send_delayed_mail(self):
        orders = self.env['fsm.order'].search([('scheduled_date_start', '<', fields.Date.today()),
                                               ('stage_id.name', '=', 'New')])
        if orders:
            template = self.env.ref('prac_doq_general.email_template_delayed_order')
            if template:
                template.with_context(orders=orders).send_mail(orders[0].id, force_send=True, raise_exception=True)
        

class FsmEquipmentLine(models.Model):
    _name = "fsm.equimnet.line"

    fsm_order_id = fields.Many2one(comodel_name='fsm.order')
    equipment_id = fields.Many2one(comodel_name='maintenance.equipment')

    @api.onchange('equipment_id')
    def _onchange_equipment_id(self):
        return {'domain': {'equipment_id':
                [('id', 'not in', self.fsm_order_id.
                 mapped('equipment_line_ids.equipment_id.id'))]}}
