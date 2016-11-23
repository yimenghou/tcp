# -*- coding: utf-8 -*-  

from FPGA_flow import FPGA_demo
from getImg import getImg
import SocketServer
import yaml

class FPGAHandler(SocketServer.BaseRequestHandler):    

    

    def handle(self): 

        print "FPGA server's ready .."
        flow_cout = 0
        task_cout = 0
        task_fifo = ''

        while True:  

            if flow_cout == 72:
                self.request.sendall( '*' )
                break

            if len(task_fifo) == 0:
                print "> Detecting data .."
                self.data = self.request.recv(8192)
                task_fifo += self.data 
                print task_fifo
                task_cout += len(self.data)
            else:
                print task_fifo
                pass

            if task_fifo[0] == '#':
                # beginning of event
                fpga0.clear()
                task_fifo = task_fifo[1:]
                print "Received request from client, start working"

            elif task_fifo[0] == '+':
                # accumulator
                fpga0.batchTrain()
                print "current train idx:", fpga0.tr_idx*100
                y_fpga = fpga0.batchTest()
                accuracy = str(y_fpga['meanAccuracy'])

                if len(accuracy) >= 4:
                    pass
                else:
                    fit_zeros = '0'*(4-len(accuracy)) 
                    accuracy += fit_zeros

                self.request.sendall( accuracy[:4] )
                task_fifo = task_fifo[1:]
                flow_cout += 1
                print "> FPGA batch training works complete"

            elif task_fifo[0].isdigit() :
                # single test
                y_fpga = fpga0.singleTest( int(task_fifo[0] )) 
                self.request.sendall( str(y_fpga['meanAccuracy']) )
                task_fifo = task_fifo[1:]
                print "> FPGA single testing works complete"

            elif task_fifo[0] == '*':
                # end of event
                y_fpga = fpga0.batchTest()
                self.request.sendall( '*' )
                flow_cout = 0                 
                break
                print "FPGA jobs done"

            else:
                flow_cout = 0
                break

if __name__ == "__main__":
    
    HOST1, PORT1 = "127.0.0.1", 15001

    config_file = "paint.yaml"
    with open(config_file, 'r') as fhandle:
        IMGconfig = yaml.load(fhandle) 
    
    imgOBJ1 = getImg(IMGconfig["dataset_paint"])
    datacontent0 = imgOBJ1.dataset
    datalabel = imgOBJ1.label

    fpga0 = FPGA_demo(datacontent0, datalabel)

    server_fpga = SocketServer.TCPServer((HOST1, PORT1), FPGAHandler) 
    server_fpga.serve_forever()

    
    
    
    
    
    
    
    
    
    
    
    
