from rest_api_demo.iControl import IControl
from getpass import getpass

ip_address = '172.30.0.100'
port = '443'
username = input('BigIP username: ')
password = getpass('BigIP password: ')
# Start the class
iControl = IControl(ip_address, port)
iControl.get_token(username,password)
iControl.list_virtual_servers()['items']
