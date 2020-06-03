from rest_api_demo.iControl import iControl
ip_address=''
port='443'
# Start the class
IControl = (ip_address,port)
iControl.f5token()
iControl.list_virtual_servers()
