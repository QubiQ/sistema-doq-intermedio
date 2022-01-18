from odoo import api, fields, models


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    weight = fields.Float(string='Name', digits='Stock Weight')

    weight_name = fields.Char(compute="_compute_weight_name")

    def _compute_weight_name(self):
        for rec in self:
            rec.weight_name = self.env['product.template']._get_weight_uom_name_from_ir_config_parameter()