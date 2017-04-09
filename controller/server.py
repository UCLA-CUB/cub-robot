import socket

import control

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serversocket.bind((socket.gethostname(), 1337))

serversocket.listen(1)

while(1):
    clientsocket,address = serversocket.accept()

    try:
        cs = control.ControlSocket(clientsocket)

        while(1):
            print cs.receiveControl()
    except Exception as e:
        print e.message
        continue
