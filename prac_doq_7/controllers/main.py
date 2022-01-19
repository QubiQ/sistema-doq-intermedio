from odoo import http
from odoo.http import request


class WebseriviceController(http.Controller):

    @http.route('/order_state', type='json', auth='public', methods=['POST'])
    def order_state(self, **post):
        result = {'error': '', 'msg': ''}
        data = request.jsonrequest
        if data.get('token') != 'doq_rule22':
            result['error'] = 'Invalid Token'
        else:
            state = request.env['sale.order'].sudo().search(
                [('name', '=', data.get('order'))]).state
            if not state:
                result['error'] = 'Sale not found'
            else:
                result['msg'] = state
        return result
