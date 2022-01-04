from odoo import api, fields, models, _
from odoo.exceptions import ValidationError



class BooksRent(models.Model):
    _name = 'books.rent'
    # 3º Historia de usuario
    partner_id = fields.Many2one(comodel_name="res.partner",
                                 domain="[('is_library_partner', '=', True)]")
    library_partner_code = fields.Char(
        string='Library Partner Code',
        related="partner_id.library_partner_code")
    book_id = fields.Many2one(comodel_name='books.book', string='Book')
    state = fields.Selection(
        string='State',
        selection=[('loan', 'On Loan'), ('returned', 'Returned')],
        default="loan",
        )
    
    loan_date = fields.Datetime(string="Loan Date", default=fields.Datetime.now())
    return_date = fields.Datetime(string="Returned Date")
    
    #Módulo 3 Wizards - Apartado 2
    active = fields.Boolean(default=True)

    @api.constrains('book_id')
    def check_book_type(self):
        for rec in self:
            if rec.book_id and rec.book_id.book_type != 'fisico':
                raise ValidationError("Only physical books can be borrowed")

    # 4º Historia de Usuario
    def return_book(self):
        for rec in self:
            rec.write({'return_date': fields.Datetime.now(),
                       'state': 'returned'})
            
    # 5º Historia de Usuario
    @api.model
    def create(self, vals):
        if 'book_id' in vals:
            book_id = self.env['books.book'].browse(vals.get('book_id'))
            if book_id.qty_available <= 0:
                raise ValidationError("You don't enough quantity to borrow this book")
        return super().create(vals)

    #Módulo 3 wizards - Apartado 1
    def launch_rate_wizard(self):
        return {
            "name":"Rate user",
            "view_mode":"form",
            "res_model":"rate.wizard",
            "target":"new",
            "type":"ir.actions.act_window"
        }
    
    def launch_print_wizard(self):
        return {
            "name":"Print report",
            "view_mode":"form",
            "res_model":"print.wizard",
            "target":"new",
            "type":"ir.actions.act_window"
        }

    #Práctica módulo 6 - Apartado 1
    def send_mail_server(self):
        
        for rent_id in self._context["active_ids"]:
            ctx = {}
            partner = self.env["books.rent"].browse(rent_id).partner_id
            ctx['email_to'] = partner.email
            ctx['email_from'] = self.env.user.work_email
            ctx['send_email'] = True
            ctx['partner_id'] = partner.name
            template = self.env.ref('practica_final_3.email_template_server_rent')
            template.with_context(ctx).send_mail(rent_id, force_send=True, raise_exception=False)
    
    #Práctica módulo 6 - Apartado 2
    def compose_email(self):
        '''
        This function opens a window to compose an email, with the emai template message loaded by default
        '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('practica_final_3', 'email_template_server_rent')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'books.rent',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'partner_id':self.partner_id.name,
            'email_to':self.partner_id.email,
            'email_from':self.env.user.work_email,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
