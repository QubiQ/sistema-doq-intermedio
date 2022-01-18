from odoo import fields, models, tools


class FsmEquipmentReport(models.Model):
    _name = 'fsm.equipment.report'
    _auto = False

    equipment_id = fields.Many2one(comodel_name='maintenance.equipment')
    order_id = fields.Many2one(comodel_name='fsm.order')
    asigned_to = fields.Many2one(comodel_name="fsm.person")
    scheduled_date_start = fields.Datetime()
    stage_id = fields.Many2one(comodel_name="fsm.stage")

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute('''CREATE OR REPLACE VIEW %s AS (
            SELECT l.id AS id,
            l.equipment_id AS equipment_id,
            l.fsm_order_id AS order_id,
            o.person_id AS asigned_to,
            o.scheduled_date_start AS scheduled_date_start,
            o.stage_id AS stage_id
            FROM fsm_equimnet_line AS l
            INNER JOIN fsm_order AS o ON o.id=l.fsm_order_id)
            ''' % self._table)
