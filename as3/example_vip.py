from as3.as3 import As3
from getpass import getpass
import json

ip_address = '172.30.0.100'
port = '443'
username = input('BigIP username: ')
password = getpass('BigIP password: ')

as3 = As3(ip_address, port, username, password)

# example of VIP and pool creation
with open('as3/as3_declarations/vip_pool_creation.json', 'r') as file:
    response = as3.http_call(http_method='POST', post_data=json.load(file))
print(response)
# example of VIP and pool deletion
with open('as3/as3_declarations/vip_pool_creation.json', 'r') as file:
    response = as3.http_call(http_method='DELTE', post_data=json.load(file))
print(response)
