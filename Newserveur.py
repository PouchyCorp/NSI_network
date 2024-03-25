from socket import socket
import pygame as pg
import _thread
import pickle

print('starting...')
server = socket()
server.bind(('127.0.0.1', 16384))
server.listen(5)
clientList = {}
players = {}
PlayerNum = 0

def on_new_client(client,PlayerNum):
    clock = pg.time.Clock()
    while True:
        clock.tick(60)
        data = pickle.loads(client.recv(2048))
        if data:
            players[PlayerNum] = data
        else:
            client.close()
            return
        
        if PlayerNum == 0:
            client.send(pickle.dumps(players[1]))
        else:
            client.send(pickle.dumps(players[2]))
        
        response = '0'
        client.send(response.encode())


run = True
while run:
    (sourceClient, addrClient) = server.accept()
    if sourceClient not in clientList:
        clientList[sourceClient] = addrClient
        print('connected clients :',clientList)
        _thread.start_new_thread(on_new_client,(sourceClient, PlayerNum))
        PlayerNum+=1

pg.quit()
