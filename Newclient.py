from socket import socket
from time import sleep
import pygame as p
from random import randint
import pickle
from player import Player
from bullet import Bullet 

print('trying to connect to server')
server = socket()
server.connect( ('127.0.0.1', 16384) )
print('connected')

p.init()
WIN = p.display.set_mode((500,500))

debugMode = False
run = True
def mainLoop():
    global run
    global debugMode

    attackSpeed = 1
    attackSpeedTimer = 1
    localPlayer : Player = pickle.loads(server.recv(2048))
    localBullets : list[Bullet] = []
    otherBulletsPos : list[tuple] = []
    OtherPlayers : dict[int, Player] = {}
    while run:

        localPlayer.move()
        localPlayer.updateValues()

        attackSpeedTimer += attackSpeed/60
        if attackSpeedTimer >= 1:
            attackSpeedTimer = 0
            localBullets.append(Bullet(localPlayer.x,localPlayer.y,localPlayer.mouseDir))
        for bullet in localBullets:
            bullet.move()
            bullet.updateValues()
        localBulletsPos : list[tuple] = [bullet.pos for bullet in localBullets]

        if debugMode:print('sending data to server')

        server.send(pickle.dumps({'player' : localPlayer,
                                   'bulletsPos' : localBulletsPos}))
        
        if debugMode:print('data sent to server')

        freshData = server.recv(2048)        
        OtherPlayers = {}
        if freshData != b'0':
            data : dict = pickle.loads(freshData)
            
            for player in data['players']:
                OtherPlayers[player.num] = player
            otherBulletsPos : list[tuple] = data['bullets']

            if debugMode:print(data)
            if debugMode:print('players recieved from server')
        else : 
            if debugMode:print('no other player from server')

        if debugMode:print(len(OtherPlayers))
        
        
       # if serverMessage:
       #     otherPlayer = Player()


        WIN.fill('black')
        p.draw.rect(WIN, "blue", localPlayer.rect)
        for player in OtherPlayers.values():
            p.draw.rect(WIN, "red", player.rect)
        for bullet in localBullets:
            p.draw.rect(WIN,'green',bullet.rect)
        for bulletPos in otherBulletsPos:
            p.draw.rect(WIN,'green',p.Rect(bulletPos[0],bulletPos[1],10,10))
        p.draw.line(WIN,'blue',localPlayer.pos, p.mouse.get_pos())
        p.display.update()

        for event in p.event.get():
                if event.type == p.QUIT:
                    run = False
                    return

mainLoop()
server.close()
p.quit()
