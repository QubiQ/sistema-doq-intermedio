from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    pending_delivery_count = fields.Integer(compute="_compute_delivery_count")

    firstname = fields.Char("First name", index=True)
    lastname = fields.Char("Last name", index=True)
    name = fields.Char(
        compute="_compute_name",
        inverse="_inverse_name",
        required=False,
        store=True,
        readonly=False,
    )
       
    def _inverse_name(self):
        for rec in self:
            name = rec.name.split(" ")
            if name:
                rec.firstname = name[0]
            if len(name) > 1:
                rec.lastname = ' '.join(name[1:])

    @api.depends("firstname", "lastname")
    def _compute_name(self):
        for rec in self:
            rec.name = " ".join(p for p in (self.firstname, self.lastname)
                                if p)

    def _compute_delivery_count(self):
        # EXEC TIME 0.0115s
        data = self.env['stock.picking'].read_group([
            ('partner_id', 'child_of', self.ids),
            ('state', 'not in', ['done', 'cancel'])
        ], ['partner_id'], ['partner_id'])
        result = dict((d['partner_id'][0], d['partner_id_count'])
                      for d in data)
        for rec in self:
            rec.pending_delivery_count = result.get(rec.id, 0)

        # ANOTHER WAY
        # EXECT TIME 0.08s
        # This way is more faster if self only contains 1 record
        # Otherwise is better to use read_group since only queries once.
        # for rec in self:
        #     rec.pending_delivery_count = rec.env['stock.picking'].\
        #         search_count([
        #             ('partner_id', 'child_of', rec.id),
        #             ('state', 'not in', ['done', 'cancel'])])

    def action_view_delivery(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "stock.stock_picking_action_picking_type")
        action['domain'] = [
            ('partner_id', 'child_of', self.id),
            ('state', 'not in', ['done', 'cancel']),
        ]
        action['context'] = {'default_parner_id': self.id}
        return action
