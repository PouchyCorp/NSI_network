from socket import socket
from sys import argv
import pygame as pg
import _thread
import pickle
from player import Player
from time import sleep

try:
    if False:
        MapName = 'Maps\\'+str(argv[1])+'.pkl'
    else:
        #override for tests
        MapName = 'Maps\\apagnan.pkl'
        
    with open(MapName,'rb') as map:
        unpickledMap = pickle.load(map)
    print('loading '+MapName+' as map')
except:
    MapName = 'Maps\\DO_NOT_DELETE.pkl'
    print('loading blank map')
    with open(MapName,'rb') as map:
        unpickledMap = pickle.load(map)


def main():
    print('waiting for client connections')
    server = socket()
    server.bind(('127.0.0.1', 12345))
    server.listen(5)
    clientList = {}
    players : dict[int, Player] = {}
    bulletsPos : dict[int, tuple] = {}
    playerNum = 0
    debugMode = False
    
    

    def on_new_client(client,playerNum : int):
        clock = pg.time.Clock()
        print('player',playerNum,'connected')

        #sending map to client
        client.send(pickle.dumps(unpickledMap))

        #client confirmation because client don't catch player data if else
        client.recv(1)
        #sending starting player class
        players[playerNum] = Player(50, 50, playerNum)
        client.send(pickle.dumps(players[playerNum]))
        while True:
            clock.tick(60)
            
            #recieve data from player
            freshData = client.recv(20480)
            if debugMode:print('data from',playerNum,' recieved by server') 

            if freshData:
                data : dict = pickle.loads(freshData)
                if debugMode:print(data)
                #unwrapping data into local variables to be redistributed to other players
                players[playerNum] = data['player']
                bulletsPos[playerNum] = data['bulletsPos']
                

            else:
                #if no data recieved, disconnect the player and close thread
                print(playerNum,' disconnected')
                del players[playerNum]
                del clientList[client]
                try:
                    del bulletsPos[playerNum]
                except:
                    pass
                
                client.close()
                return

            #sending bullets from only the other players
            playersWithoutSelf = players.copy()
            del playersWithoutSelf[playerNum]
            playersWithoutSelf = [player for player in playersWithoutSelf.values()]

            #sending bullets from only the other players
            bulletsPosWithoutSelf = bulletsPos.copy()
            del bulletsPosWithoutSelf[playerNum]
            #flatten list of list
            bulletsPosWithoutSelfList = []
            for bulletList in bulletsPosWithoutSelf.values():
                for bullet in bulletList:
                    bulletsPosWithoutSelfList.append(bullet)

            #send other players data if they exist
            if playersWithoutSelf:
                client.send(pickle.dumps({'players' : playersWithoutSelf,
                                        'bullets' :bulletsPosWithoutSelfList}))
                if debugMode:print('data sent to',playerNum)
            else:
                #if no, send blank message sign
                client.send(b'0')
                if debugMode:print('sending blank to',playerNum)
            


    run = True
    while run:
        (sourceClient, addrClient) = server.accept()
        if sourceClient not in clientList:
            clientList[sourceClient] = addrClient
            #attribute id to client and launch thread
            _thread.start_new_thread(on_new_client,(sourceClient, playerNum))
            playerNum+=1

    pg.quit()

main()
