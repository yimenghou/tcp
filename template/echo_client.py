# -*- coding: utf-8 -*-

import socket


HOST, PORT = "192.168.2.12", 10000
data = " ".join(sys.argv[1:])

# create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # connect to server 
    sock.connect((HOST, PORT))
    
    # send data
    sock.sendall( img )
    
    # receive data back from the server
    received = sock.recv( 1024 )

finally:
# shut down
    sock.close()    

#print("Sent:     {}".format(data))
#print("Received: {}".format(received))