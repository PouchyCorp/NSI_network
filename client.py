from socket import socket
from time import sleep
import pygame as pg
from random import randint

print('starting')
serveur = socket()
serveur.connect( ('192.168.56.1', 16384) )
############

WIN = pg.display.set_mode((1000,1000))

run = True
while run:
    message = serveur.recv(1000)

    keys = pg.key.get_pressed()

    reponse = "0"
    rand = 0
    if keys[pg.K_LEFT] or rand == 1:
        reponse = "LEFT"
    if keys[pg.K_RIGHT] or rand == 2:
        reponse = "RIGHT"
    if keys[pg.K_DOWN] or rand == 3:
        reponse = "DOWN"
    if keys[pg.K_UP] or rand == 4:
        reponse = "UP"

    serveur.send(reponse.encode())
    
    for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break

serveur.close()
pg.quit()
