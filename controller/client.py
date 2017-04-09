import socket
import time
import pygame

from util.control import ControlSocket

pygame.init()
screen = pygame.display.set_mode((100,100))

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(("192.168.42.1", 1337))
cs = ControlSocket(clientsocket)

def clamp(v, l, h):
    return min((max((v, l)), h))

sendcounter = 0

while(1):
    pygame.event.pump()

    pkeys = pygame.key.get_pressed()
    up,down,left,right,quit = [(1.0 if pkeys[x] else 0.0) for x in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_q]]

    if quit > 0.5:
        break

    left_motor = clamp(up + right - left - down, -1, 1) / 2 + 0.5
    right_motor = clamp(up + left - right - down, -1, 1) / 2 + 0.5

    sendcounter += 1

    if sendcounter > 5:
        cs.transmitControl({"left_motor" : left_motor, "right_motor" : right_motor})
        sendcounter = 0

clientsocket.close()
pygame.quit()
exit(0)
