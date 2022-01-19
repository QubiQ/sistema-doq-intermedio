import xmlrpc.client
import requests
# Obtenemos información de las credenciales

url = "http://localhost:14069"
db = "doc_final"
username = "admin"
password = "admin"

# Hacemos un Log in
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
# Obtenemos el objeto para operar con modelos
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Buscamos Sale Orders
sales = models.execute_kw(db, uid, password, 'sale.order',
                          'get_pending_sale_order', ['01-20-2022'])
print(sales)


json = {'token': 'doq_rule22', 'order': 'S00024'}

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

result = requests.post('http://localhost:14069/order_state', json=json, headers=headers)

print(result.json())
