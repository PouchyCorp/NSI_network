import sys
import socket
import pygame as p
import pickle
from player import Player
from bullet import Bullet 
from time import time
import homepage

p.init()
p.mixer.init()

try :
    ip = str(sys.argv[0])
    port = int(sys.argv[1])
    name = str(sys.argv[2])

except:
    ip = '127.0.0.1'
    port = 12345
    name = "Skibidi"

server = homepage.main(ip,port,name)

WIN = p.display.set_mode((0,0), p.FULLSCREEN)
WINw, WINh = WIN.get_size()

bg = p.image.load('assets/background.jpg')
bg = p.transform.scale(bg,(WINw,WINh))
bulletSprite = p.image.load('assets/bullet.png')
gunSprite = p.image.load('assets/gun.png')
playerFaceSprite = p.image.load('assets/playerFace.png')
playerGreyScaleSprite = p.image.load('assets/playerGreyScale.png')
#playerGreyScaleSprite.set_alpha(100)
gunSprite = p.transform.flip(gunSprite,True,False)
shieldSprite = p.image.load('assets/side_shield.png')
shieldSprite = p.transform.scale_by(shieldSprite,2)
deathSound = p.mixer.Sound('assets/death.mp3')
shootSound = p.mixer.Sound('assets/shoot.mp3')
hitSound = p.mixer.Sound('assets/hit.mp3')
deathSound.set_volume(1)
shootSound.set_volume(0.05)
hitSound.set_volume(0.5)

clock = p.time.Clock()
debugMode = False
run = True

def renderText(what, color, pos):
    font = p.font.Font('assets/Minecraft.ttf', 30)
    text = font.render(what, True, p.Color(color))
    WIN.blit(text, pos)

def setPlayerSprite(surface, color):
    rect = surface.get_rect()
    surf = p.Surface(rect.size)
    surf.set_alpha(255)
    surf.fill(color)

    newSurf = surface.copy()
    newSurf.blit(surf, (0, 0), None, p.BLEND_MULT)
    newSurf.blit(playerFaceSprite,(0,0))
    return newSurf

#dynamic player sprite
localPlayerSprite = setPlayerSprite(playerGreyScaleSprite,(255,0,0))
otherPlayerSprite = setPlayerSprite(playerGreyScaleSprite,'red')

def draw(localPlayer : Player,OtherPlayers,localBullets,otherBulletsPos,map,guns,shield):
    WIN.blit(bg,(0,0))
    for wall in map:
        p.draw.rect(WIN, wall['color'], wall['rect'])
    WIN.blit(localPlayerSprite,localPlayer.rect)
    WIN.blits([(otherPlayerSprite,player.rect) for player in OtherPlayers])
    WIN.blits([(bulletSprite,bullet.rect) for bullet in localBullets])
    WIN.blits([(bulletSprite,bullet) for bullet in otherBulletsPos])
    WIN.blits([(rotatedGunSprite,guns[rotatedGunSprite]) for rotatedGunSprite in guns])
    #for shield_ in shield.values():
    #    p.draw.rect(WIN,'green',shield_[1])
    WIN.blits([(rotatedShield[0],rotatedShield[1]) for rotatedShield in shield.values()])
    renderText(str(localPlayer.hp),'red',(0,0))
    #p.draw.line(WIN,'blue',localPlayer.rect.center, localPlayer.otherHandPos)

def mainLoop():
    global run
    global debugMode

    print('launching game')
    attackSpeed = 5
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

        if not localPlayer.dead:
            localPlayer.dir = localPlayer.recordInputDir()
            localPlayer.move(localPlayer.dir,map)

            localPlayer.updateValues()

            #attack speed logic
            attackSpeedTimer += attackSpeed/60
            if attackSpeedTimer >= 1 and p.mouse.get_pressed()[0]:
                p.mixer.Sound.play(shootSound)
                attackSpeedTimer = 0
                spawnDistFromPlayer = localPlayer.mouseDir.copy()
                spawnDistFromPlayer.scale_to_length(20)
                bulletSpawnPoint = (int(localPlayer.rect.centerx+spawnDistFromPlayer.x),int(localPlayer.rect.centery+spawnDistFromPlayer.y))

                localBullets.append(Bullet(bulletSpawnPoint[0],bulletSpawnPoint[1],localPlayer.mouseDir.normalize()))


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
        freshData = server.recv(10000)        
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
                #hit collision detection
                if hitPlayer.num == localPlayer.num:
                    p.mixer.Sound.play(hitSound)
                    localPlayer.hp-=1

            #death system
            if player.hp <= 0 and not player.dead:
                p.mixer.Sound.play(deathSound)
                if player.num == localPlayer.num:
                    localPlayer.dead = True
                    localPlayer.rect.x, localPlayer.rect.y= 10000,10000
                    localPlayer.updateValues()

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
        
        if localPlayer.dead:
            p.transform.grayscale(WIN,WIN)
        p.display.update()

mainLoop()
server.close()
p.mixer.quit()
p.quit()
