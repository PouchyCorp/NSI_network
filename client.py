import sys
from socket import socket
import pygame as p
import pickle
from player import Player
from bullet import Bullet 
from time import time

try:
    IP = str(sys.argv[1])
    PORT = int(sys.argv[2])
except:
    IP = '127.0.0.1'
    PORT = 12345

print('trying to connect to server')
server = socket()
server.connect((IP, PORT))
print('connected')

p.init()
WIN = p.display.set_mode((1080,1080))
clock = p.time.Clock()
debugMode = False
run = True

def renderText(what, color, pos):
    font = p.font.Font('Minecraft.ttf', 30)
    text = font.render(what, True, p.Color(color))
    WIN.blit(text, pos)

def draw(localPlayer,OtherPlayers,localBullets,otherBulletsPos,map):
    WIN.fill('black')
    for wall in map:
        p.draw.rect(WIN, wall['color'], wall['rect'])
    p.draw.rect(WIN, "blue", localPlayer.rect)
    for player in OtherPlayers:
        p.draw.rect(WIN, "red", player.rect)
    for bullet in localBullets:
        p.draw.rect(WIN,'green',bullet.rect)
    for bulletPos in otherBulletsPos:
        p.draw.rect(WIN,'green',p.Rect(bulletPos[0],bulletPos[1],10,10))
    renderText(str(localPlayer.hp),'red',(0,0))
    p.draw.line(WIN,'blue',localPlayer.pos, p.mouse.get_pos())

def mainLoop():
    global run
    global debugMode

    attackSpeed = 1
    attackSpeedTimer = 1
    map : list = pickle.loads(server.recv(2048))
    mapColliders = [wall['rect'] for wall in map]
    print('map loaded')
    localPlayer : Player = pickle.loads(server.recv(2048))
    print('player loaded')
    localBullets : list[Bullet] = []
    otherBulletsPos : list[tuple] = []
    while run:
        timerStart = time()
        #local player updates
        localPlayer.dir = localPlayer.recordInputDir()
        localPlayer.move(localPlayer.dir,mapColliders)
        localPlayer.updateValues()

        #attack speed logic
        attackSpeedTimer += attackSpeed/60
        if attackSpeedTimer >= 1:
            attackSpeedTimer = 0
            localBullets.append(Bullet(localPlayer.x,localPlayer.y,localPlayer.mouseDir))

        #local bullet updates
        for bullet in localBullets:
            bullet.move(mapColliders)
            bullet.updateValues()
        localBulletsPos : list[tuple] = [bullet.pos for bullet in localBullets]

        if debugMode:print('sending data to server')

        #sending data to server
        server.send(pickle.dumps({'player' : localPlayer,
                                   'bulletsPos' : localBulletsPos}))
        
        if debugMode:print('data sent to server')

        #recieve data
        freshData = server.recv(4056)        
        OtherPlayers : list[Player] = []
        #check if blank message sign
        if freshData != b'0':
            data : dict = pickle.loads(freshData)
            
            #unwrapping data into local variables
            OtherPlayers : list[Player] = data['players']
            otherBulletsPos : list[tuple] = data['bullets']

            if debugMode:print(data)
            if debugMode:print('players recieved from server')
        else : 
            if debugMode:print('no other player from server')

        if debugMode:print(len(OtherPlayers))
        

        draw(localPlayer,OtherPlayers,localBullets,otherBulletsPos,map)

        for event in p.event.get():
                if event.type == p.QUIT:
                    run = False
                    return
        timerEnd = time()
        timerFluctuation = round((timerEnd-timerStart)/(1/60),2)
        renderText('fps fluctuation :'+str(timerFluctuation),'white',(0,100))
        
        p.display.update()

mainLoop()
server.close()
p.quit()
