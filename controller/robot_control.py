#!/usr/bin/python

import smbus
import socket
import signal

from util.motor import MotorController
from util.control import ControlSocket

DEV_ADDR = 0x40

sockets = []

def signal_handler(signal, frame):
    global sockets
    
    "Killing connection and exiting..."

    for s in sockets:
        s.close()

    sockets = []

    exit(0)

signal.signal(signal.SIGINT, signal_handler) 

# Initialize smbus and motor controller
bus = smbus.SMBus(1)
mc = MotorController(bus, DEV_ADDR)
l_motor,r_motor = mc.motors[0:2]

# Open listening server socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(("192.168.42.1", 1337))
serversocket.listen(1)

sockets.append(serversocket)

while(1):
    clientsocket,address = serversocket.accept()

    sockets.append(clientsocket)

    try:
        cs = ControlSocket(clientsocket)

        while(1):
            cdict = cs.receiveControl()

            print cdict

            l_motor.retry_write(cdict["left_motor"])
            r_motor.retry_write(cdict["right_motor"])

    except Exception as e:
        print e.message
        continue

    clientsocket.close() 

for s in sockets:
    s.close()

sockets = []
