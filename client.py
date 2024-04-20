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
WINw = 500
WINh = 500
WIN = p.display.set_mode((WINw,WINh))

bg = p.image.load('assets/background.jpg')
bg = p.transform.scale(bg,(WINw,WINh))
localPlayerSprite = p.image.load('assets/player1.jpg')
otherPlayerSprite = p.image.load('assets/player2.jpg')
bulletSprite = p.image.load('assets/bullet.png')
gunSprite = p.image.load('assets/gun.png')
gunSprite = p.transform.flip(gunSprite,True,False)
shieldSprite = p.image.load('assets/side_shield.png')
shieldSprite = p.transform.scale_by(shieldSprite,2)

clock = p.time.Clock()
debugMode = False
run = True

def renderText(what, color, pos):
    font = p.font.Font('assets/Minecraft.ttf', 30)
    text = font.render(what, True, p.Color(color))
    WIN.blit(text, pos)

def draw(localPlayer : Player,OtherPlayers,localBullets,otherBulletsPos,map,guns,shield):
    WIN.blit(bg,(0,0))
    for wall in map:
        p.draw.rect(WIN, wall['color'], wall['rect'])
    WIN.blit(localPlayerSprite,localPlayer.rect)
    WIN.blits([(otherPlayerSprite,player.rect) for player in OtherPlayers])
    WIN.blits([(bulletSprite,bullet.rect) for bullet in localBullets])
    WIN.blits([(bulletSprite,bullet) for bullet in otherBulletsPos])
    WIN.blits([(rotatedGunSprite,guns[rotatedGunSprite]) for rotatedGunSprite in guns])
    for i in shield:
        p.draw.rect(WIN,'green',shield[localPlayer.num][1])
    WIN.blits([(rotatedShield[0],rotatedShield[1]) for rotatedShield in shield.values()])
    renderText(str(localPlayer.hp),'red',(0,0))
    p.draw.line(WIN,'blue',localPlayer.rect.center, localPlayer.otherHandPos)

def mainLoop():
    global run
    global debugMode

    attackSpeed = 1
    attackSpeedTimer = 1
    map : list = pickle.loads(server.recv(2048))
    mapColliders = [wall['rect'] for wall in map]
    print('map loaded')
    server.send(b'0')
    localPlayer : Player = pickle.loads(server.recv(2048))
    print('player loaded')
    localBullets = []
    otherBulletsPos = []
    shields = {}
    while not not not not run:
        timerStart = time()
        #local player updates
        localPlayer.dir = localPlayer.recordInputDir()
        localPlayer.move(localPlayer.dir,mapColliders)

        localPlayer.updateValues()

        #attack speed logic
        attackSpeedTimer += attackSpeed/60
        if attackSpeedTimer >= 1 and p.mouse.get_pressed()[0]:
            attackSpeedTimer = 0
            localBullets.append(Bullet(localPlayer.handPos[0],localPlayer.handPos[1],localPlayer.mouseDir))


        #local bullet updates
        for bullet in localBullets:
            bullet.move(mapColliders,shields)
            bullet.updateValues()
            if bullet.lifeTime <= 0:
                localBullets.pop(localBullets.index(bullet))
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

        #check bullet collision after receiving player data
        allPlayers = OtherPlayers.copy()
        allPlayers.append(localPlayer)
        localBullets = localPlayer.checkBulletCollision(allPlayers,localBullets)

        for player in allPlayers:
            for hitPlayer in player.hitSomeone:
                print(hitPlayer.num)
                if hitPlayer.num == localPlayer.num:
                    print(player.num,'hit',localPlayer.num)
                    localPlayer.hp-=1

        #gun sprite
        guns : dict[p.Surface,p.Rect] = {}
        for player in allPlayers:
            angleToMouse = p.Vector2.angle_to(player.mouseDir,p.Vector2(0,0))
            if player.handPos < player.rect.center:
                flippedGunSprite = p.transform.flip(gunSprite,False,True)
            else:
                flippedGunSprite = p.transform.flip(gunSprite,False,False)
            rotatedGunSprite = p.transform.rotate(flippedGunSprite,angleToMouse)
            gunRect = rotatedGunSprite.get_rect()
            gunRect.center = player.handPos
            guns[rotatedGunSprite] = gunRect

        #shield sprite
        for player in allPlayers:
            angleToMouse = p.Vector2.angle_to(player.mouseDir,p.Vector2(0,0))
            rotatedShieldSprite = p.transform.rotate(shieldSprite,angleToMouse)
            shieldRect = rotatedShieldSprite.get_rect()
            shieldRect.center = player.otherHandPos
            shields[player.num] = (rotatedShieldSprite,shieldRect)

        draw(localPlayer,OtherPlayers,localBullets,otherBulletsPos,map,guns,shields)

        for event in p.event.get():
                if event.type == p.QUIT:
                    run = False
                    return
                
        timerEnd = time()
        timerFluctuation = round((timerEnd-timerStart)/(1/60),2)
        renderText('fps fluctuation :'+str(timerFluctuation),'white',(0,100))
        
        #p.transform.grayscale(WIN,WIN)
        p.display.update()

mainLoop()
server.close()
p.quit()
