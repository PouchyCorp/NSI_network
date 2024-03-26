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

def on_new_client(client,PlayerNum):
    clock = pg.time.Clock()
    client.send(pickle.dumps(Player(50, 50)))
    while True:
        clock.tick(60)
        msg = client.recv(20480)
        if msg:
            data = pickle.loads(msg)
            players[PlayerNum] = msg
        else:
            client.close()
            return
        if len(players) > 1:
            if PlayerNum == 0:
                client.send(players[1])
            else:
                client.send(players[0])
            
        #response = ''
        #client.send(response.encode())


run = True
while run:
    (sourceClient, addrClient) = server.accept()
    if sourceClient not in clientList:
        clientList[sourceClient] = addrClient
        print('connected clients :',clientList)
        _thread.start_new_thread(on_new_client,(sourceClient, PlayerNum))
        PlayerNum+=1

pg.quit()
