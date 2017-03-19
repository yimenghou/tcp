# -*- coding: utf-8 -*-  
import SocketServer
import socket  
import threading  
import time  
        

class MyTCPSocketHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024)
        print("{} wrote:".format(self.client_address[0])), self.data

        # just send back the same data, but upper-cased
        self.request.sendall( "Greetings from Yimeng! "+"Your Data:"+str(self.data) )

if __name__ == "__main__":
    
    HOST, PORT = "192.168.2.17", 15051

    # instantiate the server, and bind to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPSocketHandler)

    # activate the server
    # this will keep running until Ctrl-C
    server.serve_forever()
