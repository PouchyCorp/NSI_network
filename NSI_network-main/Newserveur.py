from socket import socket
import pygame as pg
import _thread
import pickle
from player import Player

print('waiting for client connections')
server = socket()
server.bind(('127.0.0.1', 16384))
server.listen(5)
clientList = {}
players = {}
PlayerNum = 0

def on_new_client(client,PlayerNum : int):
    clock = pg.time.Clock()
    players[PlayerNum] = Player(50, 50, PlayerNum)
    client.send(pickle.dumps(players[PlayerNum]))
    while True:
        clock.tick(60)

        data = client.recv(1000)
        print('data from',PlayerNum,' recieved by server')

        if data:
            players[PlayerNum] = pickle.loads(data)
        else:
            client.close()
            return
        
        playersWithoutSelf : dict[int, Player] = players.copy()
        del playersWithoutSelf[PlayerNum]

        if playersWithoutSelf:
            for otherPlayerNum in playersWithoutSelf.keys():
                client.send(pickle.dumps(players[otherPlayerNum]))
                print('player from',otherPlayerNum,' sent to',PlayerNum)
        else:
            client.send(b'0')
            print('sending blank to',PlayerNum)
        


run = True
while run:
    (sourceClient, addrClient) = server.accept()
    if sourceClient not in clientList:
        clientList[sourceClient] = addrClient
        print('connected clients :',PlayerNum)
        _thread.start_new_thread(on_new_client,(sourceClient, PlayerNum))
        PlayerNum+=1

pg.quit()
