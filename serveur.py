from socket import socket
from time import sleep
import pygame as pg

print('starting...')
serveur = socket()
serveur.bind(('192.168.56.1', 16384))
serveur.listen()
(sclient, adclient) = serveur.accept()
if sclient:
    print('connected')

WIN = pg.display.set_mode((1000,1000))
clock = pg.time.Clock()

rectX = 100
rectY = 100
player = pg.Rect(50,50,rectX,rectY)

def draw(player):
    WIN.fill('black')
    pg.draw.rect(WIN, "red", player)
    pg.display.update()

##########
run = True
while run:
    clock.tick(60)

    reponse = '0'
    sclient.send(reponse.encode())

    message = sclient.recv(1000)

    reponse = message.decode()
    print(reponse)

    for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
    
    if reponse == "LEFT":
        player.x -= 1
    if reponse == "RIGHT":
        player.x += 1
    if reponse == "UP":
        player.y -= 1
    if reponse == "DOWN":
        player.y += 1

    draw(player)

sclient.close()
pg.quit()
