from odoo import api, fields, models
from odoo.exceptions import UserError



class ResPartner(models.Model):
    _inherit = 'res.partner'
    # 1º Historia de usuario
    is_library_partner = fields.Boolean(string='Is Library Partner')
    library_partner_code = fields.Char(string='Library Partner Code')
    
    #Módulo wizards 
    can_rent = fields.Boolean(default=True)
    
    _sql_constraints = [
        ('library_partner_code_unique', 'unique (library_partner_code,company_id)', 'The Library Partner Code of contact must be unique per company !')
    ]
    
    #Módulo 3 Wizards - Apartado 2
    rate = fields.Float(compute = "_compute_mean_value", store=True)
    rating_ids = fields.One2many(comodel_name="rate.partner", inverse_name="partner_id", invisible="1")
    
    def singup(self):
        return {
            'name':'Sign up',
            'type':'ir.actions.act_window',
            'view_mode':'form',
            'res_model':'signup.wizard',
            'target':'new'
        }
        
    def launch_rent_wizard(self):
        return {
            'name':'Rent a book',
            'type':'ir.actions.act_window',
            'view_mode':'form',
            'res_model':'rent.book.wizard',
            'target':'new'
        }
        
    def launch_return_wizard(self):
        return {
            'name':'Return a book',
            'type':'ir.actions.act_window',
            'view_mode':'form',
            'res_model':'return.book.wizard',
            'target':'new'
        }

    # 2º Historia de usuario
    def dropout(self):
        self.write({'is_library_partner': False,
                    'library_partner_code': False})
        
    # 6º Historia de Usuario
    def unlink(self):
        for rec in self:
            if rec.is_library_partner:
                if self.env['books.rent'].search(
                    [('partner_id', '=', rec.id),
                     ('state', '=', 'loan')]):
                    raise UserError(
                        "The partner %s still has books to return" % rec.name)
        return super().unlink()
    
    # 7º Historia de Usuario
    def get_books(self):
        # Esto lo hago para asegurarme de este método se lance desde un registro
        # len(self) == 1
        self.ensure_one()
        return self.env['books.rent'].search([('partner_id', '=', self.id),
                                              ('state', '=', 'loan')])
    
    #Módulo 3 wizards - Apartado 2
    @api.depends('rating_ids')
    def _compute_mean_value(self):
        for rec in self:
            if len(rec.rating_ids) > 0:
                rec.rate = sum(rec.rating_ids.mapped('rent_rate'))/len(rec.rating_ids)
            else:
                rec.rate = 0   

    #Módulo 3 wizards - Apartado 3
    def get_books_to_print(self):
        return self.env["books.rent"].search([('partner_id', '=', self.id)])

#Módulo 3 wizards - Apartado 2        
class RatePartner(models.Model):
    _name = "rate.partner"
    description = "Aux class made in order to control ratings and rent counts."
    
    partner_id = fields.Many2one(comodel_name="res.partner")
    rent_rate = fields.Integer()
