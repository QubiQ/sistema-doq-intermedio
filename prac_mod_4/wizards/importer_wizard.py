from odoo import fields, models, exceptions

import base64
import csv
from io import StringIO

import logging
_logger = logging.getLogger(__name__)


class ImporterWizard(models.TransientModel):
    _name = 'importer.wizard'

    data = fields.Binary(string='File', required=True)
    name = fields.Char(string='Filename')
    delimeter = fields.Char(
        string='Delimiter',
        default=';',
        help='Default delimiter ";"',
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True
    )

    use_jobs = fields.Boolean()
    
    
    _MAPPER = {'nif': 'vat',
               'nombre': 'name',
               'compañia': 'company_type',
               'movil': 'mobile',
               'correo': 'email',
               'categorias': 'category_id',
               'plazos_pago': 'property_payment_term_id',
               'cuenta_bancaria': 'bank_ids'}

    # Transform Functions
    def _prepare_bank_account(self, acc):
        
        bank = acc.split('-')[0][:-1] # Remove spaces
        account = acc.split('-')[1][1:]
        bank_obj = self.env['res.bank'].search([('name', '=', bank)])
        if not bank_obj:
            bank_obj = bank_obj.create({'name': bank})
        return {'bank_ids': [(0, 0, {'bank_id': bank_obj.id, 'acc_number': account})]}
    
    def _prepare_tag_ids(self, tags):
        tags_ids = []
        cat_obj = self.env['res.partner.category']
        for t in tags.split(','):
            cat_obj = cat_obj.search([('name', '=', t)])
            if not cat_obj:
                cat_obj = cat_obj.create({'name': t})
            tags_ids.append(cat_obj.id)
        return {'category_id': [(6, 0, tags_ids)]}
        
    def _prepare_address(self, address):
        address_list = address.split(',')
        cp = address_list[1].split('-')[0][1:-1] # remove spaces
        city = address_list[1].split('-')[1][1:]
        if len(address_list) > 2:
            state_id = self.env['res.country.state'].search([(
                'name', '=', address_list[2][1:]
            )])
            state_id = state_id.id if state_id else False
        return {'street':address_list[0], 'zip': cp, 'city': city, 'state_id': state_id}

    # Prepare contacts for the company
    def _prepare_child_ids(self, values):
        return {'child_ids': [(0, 0, {
            'name': values['nombre_contacto'],
            'email': values.get('email_contacto'), # If doesn't exists return False its accepted in Odoo for Strings
            'mobile': values.get('movil_contacto')
        })]}

    '''
        Function to transform and correct some values.

        :param values: Dict with the values to import.

        :return Dict with the modified values modifieds.
    '''
    def _prepare_values(self, values):
        new_values = {}
        for k, v in self._MAPPER.items():
            new_values[v] = values[k]

        if values.get('compañia'):
            new_values.update({'company_type': 'company' if values['compañia'] == "Si" else 'person'})
        if values.get('direccion'):
            new_values.update(self._prepare_address(values['direccion']))
        if values.get('pais'):
            country_id = self.env['res.country'].search([('code', '=', values['pais'])], limit=1)
            new_values.update({'country_id': country_id.id if country_id else False})
        if values.get('cuenta_bancaria'):
            new_values.update(self._prepare_bank_account(values['cuenta_bancaria']))

        if values.get('categorias'):
            new_values.update(self._prepare_tag_ids(values['categorias']))

        if values.get('plazos_pago'):
            pay_terms = self.env['account.payment.term'].search([('name', '=', values['plazos_pago'])], limit=1)
            new_values.update({'property_payment_term_id': pay_terms.id or False})

        if values.get('nombre_contacto'):
            new_values.update(self._prepare_child_ids(values))

        return self._create_partner(new_values)

    
    #This functions is to clear some fields in case we have to update
    def _clean_fields(self, partner):
        partner.bank_ids.unlink()
        partner.child_ids.unlink()

    # LOAD functions
    def _create_partner(self, values):
        partner_obj = self.env['res.partner'].search([('vat', '=', values.get('vat'))], limit=1)
        if not partner_obj:
            msg = "Created "
            partner_obj = partner_obj.create(values)
        else:
            msg = "Updated "
            self._clean_fields(partner_obj)
            partner_obj.write(values)
        return msg + str(partner_obj.id)
    '''
        Function to read the csv file and convert it to a dict.

        :return Dict with the columns and its value.
    '''
    def action_import(self):
        """Load Inventory data from the CSV file."""
        if not self.data:
            raise exceptions.Warning(_("You need to select a file!"))
        # We set up the company for work on
        self = self.with_company(self.company_id)
        # Decode the file data
        data = base64.b64decode(self.data).decode('utf-8')
        file_input = StringIO(data)
        file_input.seek(0)

        reader_info = []
        if self.delimeter:
            delimeter = str(self.delimeter)
        else:
            delimeter = ','
        reader = csv.reader(file_input, delimiter=delimeter,
                            lineterminator='\r\n')
        try:
            reader_info.extend(reader)
        except Exception:
            raise exceptions.Warning(_("Not a valid file!"))
        keys = reader_info[0]

        # Get column names
        keys_init = reader_info[0]
        keys = []
        for k in keys_init:
            temp = k.replace(' ', '_')
            keys.append(temp)

        del reader_info[0]
        values = {}
        # We duplicate the code to avoid use if inside the loop
        if self.use_jobs:
            for i in range(len(reader_info)):
                # Don't read rows that start with ( , ' ' or are empty
                if not (reader_info[i][0] is '' or reader_info[i][0][0] == '('
                        or reader_info[i][0][0] == ' '):
                    field = reader_info[i]
                    values = dict(zip(keys, field))
                    self.with_delay()._prepare_values(values)
        else:
            for i in range(len(reader_info)):
                # Don't read rows that start with ( , ' ' or are empty
                if not (reader_info[i][0] is '' or reader_info[i][0][0] == '('
                        or reader_info[i][0][0] == ' '):
                    field = reader_info[i]
                    values = dict(zip(keys, field))
                    self._prepare_values(values)

        return {'type': 'ir.actions.act_window_close'}
