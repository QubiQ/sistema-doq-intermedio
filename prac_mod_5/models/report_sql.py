from odoo import api, fields, models, tools

#Práctica módulo 5 - Vistas
class ReportSql(models.Model):
    _name = 'report.sql'
    _description = 'Class made to practise SQL model creation.'
    _auto = False

    book_name = fields.Char("Book")
    isbn = fields.Char("ISBN")
    partner_name = fields.Char("User name")
    partner_code = fields.Char("Code")
    partner_rating = fields.Float("Rating")
    
    def init(self):
        tools.drop_view_if_exists(self._cr, "report_sql")
        self._cr.execute(""" CREATE OR REPLACE VIEW report_sql AS (
            SELECT 
            row_number() OVER () as id,
            b.name as book_name, 
            b.barcode as isbn, 
            p.name as partner_name, 
            p.library_partner_code as partner_code, 
            p.rate as partner_rating 
            FROM books_rent r 
            LEFT JOIN books_book b ON (r.book_id = b.id) 
            LEFT JOIN res_partner p ON (r.partner_id = p.id))""")

    def print_report(self):

        all_entries = self.env["report.sql"].search([])
        
        #si quiero que me haga print solo la entry del que he hecho click le paso self
        #si quiero que me printee todas las entradas le paso all_entries
        return self.env.ref("practica_final_3.report_sql").report_action(self)