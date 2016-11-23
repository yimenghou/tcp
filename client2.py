# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 19:11:37 2016

@author: westwell
"""


import socket
import sys
import multiprocessing
import matplotlib.pylab as plt
from scipy import signal
import yaml
import numpy as np
import time
import SocketServer


def dataReceiver(queue):

    HOST, PORT = "127.0.0.1", 15001
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recv_result = []
    recv_iter = 0

    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))

        while True:
            # incoming data catcher
            recv_data = sock.recv(1024) 
            if len(recv_data) == 0:
                continue

            if recv_data == '*':
                print "Receiving complete"
                break
            else:
                print "Received Number %d data packages from FPGA server..."%recv_iter
                recv_result.append( recv_data )
                queue.put(recv_data)   
                recv_iter += 1
    finally:    
        sock.close()  

def dataTransmitter(queue):
    
    HOST, PORT = "127.0.0.1", 15001
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
    sock.connect((HOST, PORT))
    sock.sendall('#')

    n_cout = 0
    while True:    

        if n_cout == 71:
            print "End of Receiving"
            break

        try:
            tx_data = '0'
            sock.sendall(tx_data) 
            time.sleep(1)

        except KeyboardInterrupt:
                
            instruction = raw_input()
            if instruction == 'quit':
                sock.sendall('*')

        n_cout += 1 

    sock.close()

def transciver(queue):

    recv_data = ''
    HOST, PORT = "127.0.0.1", 15001
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
    sock.connect((HOST, PORT))
    sock.sendall('#')
    print "sent begin flag to FPGA server"

    n_cout = 0
    while True:    

        if n_cout <  72:

            try:
                tx_data = '+'
                sock.sendall(tx_data) 
                print "sent accumulator to FPGA server"

            except KeyboardInterrupt:
                    
                instruction = raw_input()
                if instruction == 'quit':
                    sock.sendall('*')

            n_cout += 1 

        else:

            if len(recv_data) == 72*4+1:
                pass
            else:
                recv_temp = sock.recv(1024)

                try:
                    recv_float = float(recv_temp)
                except ValueError:
                    continue

                queue.put(recv_float)
                recv_data += recv_temp

            if '*' in recv_temp:
                print "Receiving complete"
                break 

    sock.close()

def plotFPGAHandler(input_fpga):

    plt.figure()
    plt.ion() 
    fpga_temp = []
    batch_size = 100
    data_len = 72

    print "FPGA Accuracy plotted"
    
    i = 1
    while len(fpga_temp) < data_len:
        time.sleep(0.01)

        fpga_temp.append( float( input_fpga.get() ) )

        y_fpga = np.array(fpga_temp)

        b, a = signal.butter(2, 0.05)
        if i>=10:
            y_flt = signal.filtfilt(b,a, y_fpga, method='gust')
        else:
            y_flt = y_fpga

        plt.clf()
        plt.title("FPGA Performance")
        plt.ylabel('Accuracy')
        plt.xlabel('Training examples')
        plt.axis([0, 7200, 0, 1.2])
        plt.grid()
        line1, =plt.plot(np.arange(0,i*batch_size,batch_size), y_fpga, 'r.-', lw=1, label='Original')
        line2, =plt.plot(np.arange(0,i*batch_size,batch_size), y_flt, 'b.-', lw=1, label='Filtered') 
        plt.legend(loc=4)
        plt.show()                 
        plt.pause(0.005)
        i += 1

if __name__ == '__main__':

    recv_queue = multiprocessing.Queue()    
    
    # p0 = multiprocessing.Process(target = dataReceiver, args=(recv_queue, ))
    # p1 = multiprocessing.Process(target = dataTransmitter, args=(recv_queue, ))
    # p1 = multiprocessing.Process(target = transciver, args=(recv_queue, ))
    # p2 = multiprocessing.Process(target = plotFPGAHandler, args=(recv_queue, ))
    
    # p1.start()
    # p2.start()

    # p1.join()
    # p2.join()

    recv_data = ''
    HOST, PORT = "127.0.0.1", 15001
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
    sock.connect((HOST, PORT))
    sock.sendall('#')

    
    n_cout = 0
    while True:    

        if n_cout <  72:

            try:
                tx_data = '+'
                time.sleep(0.1)
                sock.sendall(tx_data) 
                print "sent No. %d + to FPGA server"%(n_cout+1)

            except KeyboardInterrupt:
                    
                instruction = raw_input()
                if instruction == 'quit':
                    sock.sendall('*')

            n_cout += 1 

        else:

            if len(recv_data) == 72*4+1:
                pass
            else:
                recv_temp = sock.recv(1024)

                try:
                    recv_float = float(recv_temp)
                except ValueError:
                    continue

                recv_data += recv_temp

            if '*' in recv_temp:
                print "Receiving complete"
                break 
    
    sock.close()