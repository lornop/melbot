#!/bin/python3

"""phone.py"""

import socket
import json

def read(child_conn):

    UDP_IP = ""
    UDP_PORT = 5005

    ldir = 'F'
    rdir = 'F'

    ldis = 0 #joystick mid position
    rdis = 0

    but = '-'

    sock = socket.socket(socket.AF_INET, #Internet
    socket.SOCK_DGRAM) #UDP

    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addre = sock.recvfrom(1024) #buffer size 1024 bytes
        #print("recieved message: %s" % data)
        mydict = json.loads(data)
        #print(mydict)

        #print(mydict['LDir'] + ' ' + str(mydict['LLen']) + ' ' + mydict['RDir'] + ' ' + str(mydict['RLen'])+ ' ' + mydict['But'])
        stickValue = [ mydict['LDir'], mydict['LLen'], mydict['RDir'], mydict['RLen'], mydict['But'] ]
        child_conn.send(stickValue)







# Using the special variable
# __name__
if __name__=="__main__":
    read()        	