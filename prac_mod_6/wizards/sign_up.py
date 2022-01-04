from odoo import fields, models


class signup_wizard(models.TransientModel):
    _name = 'signup.wizard'
    _description = 'Wizard that controls the sign up process.'

    code = fields.Char(string='Library partner code')
    
    def sign_up(self):
        
        partner_id = self._context["active_id"]
        self.env["res.partner"].browse(partner_id).write({'is_library_partner': True, 'library_partner_code':self.code})
