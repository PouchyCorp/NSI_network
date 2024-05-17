import socket
from sys import argv
import pygame as pg
import _thread
import pickle
from player import Player
from time import sleep

try:
    if False:
        MapName = 'Maps/'+str(argv[1])+'.pkl'
    else:
        #override for tests
        MapName = 'Maps/blockyMap.pkl'
        
    with open(MapName,'rb') as map:
        unpickledMap = pickle.load(map)
    print('loading '+MapName+' as map')
except:
    MapName = 'Maps/DO_NOT_DELETE.pkl'
    print('loading blank map')
    with open(MapName,'rb') as map:
        unpickledMap = pickle.load(map)

class Client:
    def __init__(self, num, source, addr) -> None:
        self.num = num
        self.source = source
        self.addr = addr
        self.ready = False
        self.playerColor = 'red'
        self.name = ''


IP, PORT = '' , 12345
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen()
print(f"Listening on port: {PORT}")
print('waiting for client connections')
clientList : dict[int, Client] = {}
players : dict[int, Player] = {}
bulletsPos : dict[int, tuple] = {}
playerNum = 0
debugMode = False

waiting = True

def homepage_handeling_thread():
    global waiting
    while waiting:
        asyncClientList = clientList.copy()
        for client in asyncClientList.values():
            client.source.send(b'0')
            if debugMode:print('clock signal sent')

            sleep(0.5)

            try :
                clientStatusAgglo : str = client.source.recv(100).decode()
            except:
                print(f'client {client.num} crashed')
                del asyncClientList[client.num]
                continue
            if debugMode:print(f'info recieved from client {client.num}: {clientStatusAgglo}')
            client.ready, client.playerColor = clientStatusAgglo.split('/') if clientStatusAgglo.split('/') else ['0', 'red']

            if client.ready == '1':
                client.ready = True
            else:
                client.ready = False
            print(client.ready)
            

        if clientList:
            readyToLaunchGame = True
            for client in clientList.values():
                if client.ready == False:
                    readyToLaunchGame = False
        else:
            readyToLaunchGame = False
        
        if readyToLaunchGame:
            waiting = False
            for client in clientList.values():
                client.source.send(b'1')
            if debugMode: print('attempting to launch game')
        

    print('waiting finished')
    for client in clientList.values():
            _thread.start_new_thread(on_new_client,(client.source, client.num, client.playerColor))
        
        #if debugMode:print('waiting',waiting)

def on_new_client(client,playerNum : int, color):
    print(f"lauching player {playerNum}'s game")
    clock = pg.time.Clock()

    #sending map to client
    client.send(pickle.dumps(unpickledMap))

    #client confirmation because client don't catch player data if else
    client.recv(1)
    #sending starting player class
    players[playerNum] = Player(50, 50, playerNum, color)
    client.send(pickle.dumps(players[playerNum]))
    
    run = True
    while run:
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

        #check if a player won
        flag = None
        gameOverStatusCounter = 0
        for player in players.values():
            if player.dead == True:
                gameOverStatusCounter +=1
        if gameOverStatusCounter >= len(players.values())-1:
            flag = 'GameOver'
            run = False

        #send other players data if they exist
        if playersWithoutSelf:
            client.send(pickle.dumps({'flags' : flag,
                                    'players' : playersWithoutSelf,
                                    'bullets' :bulletsPosWithoutSelfList}))
            if debugMode:print('data sent to',playerNum)
        else:
            #if no, send blank message sign
            client.send(b'0')
            if debugMode:print('sending blank to',playerNum)
            
    if flag == 'GameOver':
        _thread.start_new_thread(homepage_handeling_thread,())
    
        
        

_thread.start_new_thread(homepage_handeling_thread,())
while waiting :
    (sourceClient, addrClient) = server.accept()
    #if sourceClient not in clientList:
    clientList[playerNum] = Client(playerNum, sourceClient,addrClient)
    print(f'player {playerNum} connected')
    playerNum+=1
        

pg.quit()
