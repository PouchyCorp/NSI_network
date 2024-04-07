from socket import socket
import pygame as pg
import _thread
import pickle
from player import Player
from bullet import Bullet

print('waiting for client connections')
server = socket()
server.bind(('127.0.0.1', 16384))
server.listen(5)
clientList = {}
players : dict[int, Player] = {}
bulletsPos : dict[int, tuple] = {}
playerNum = 0
debugMode = False

def on_new_client(client,playerNum : int):
    clock = pg.time.Clock()
    print('player',playerNum,'connected')
    players[playerNum] = Player(50, 50, playerNum)
    client.send(pickle.dumps(players[playerNum]))
    while True:
        clock.tick(60)

        freshData = client.recv(20480)
        if debugMode:print('data from',playerNum,' recieved by server') 

        if freshData:
            data : dict = pickle.loads(freshData)
            if debugMode:print(data)
            players[playerNum] = data['player']
            bulletsPos[playerNum] = data['bulletsPos']
        else:
            print(playerNum,' disconnected')
            del players[playerNum]
            client.close()
            return
        
        playersWithoutSelf = players.copy()
        del playersWithoutSelf[playerNum]
        playersWithoutSelf = [player for player in playersWithoutSelf.values()]

        bulletsPosWithoutSelf = bulletsPos.copy()
        del bulletsPosWithoutSelf[playerNum]
        bulletsPosWithoutSelfList = []
        for bulletList in bulletsPosWithoutSelf.values():
            for bullet in bulletList:
                bulletsPosWithoutSelfList.append(bullet)

        if playersWithoutSelf:
            client.send(pickle.dumps({'players' : playersWithoutSelf,
                                       'bullets' :bulletsPosWithoutSelfList}))
            if debugMode:print('player from sent to',playerNum)
        else:
            client.send(b'0')
            if debugMode:print('sending blank to',playerNum)
        


run = True
while run:
    (sourceClient, addrClient) = server.accept()
    if sourceClient not in clientList:
        clientList[sourceClient] = addrClient
        _thread.start_new_thread(on_new_client,(sourceClient, playerNum))
        playerNum+=1

pg.quit()
