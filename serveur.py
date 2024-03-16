from socket import socket
import pygame as pg
from threading import Thread

print('starting...')
server = socket()
server.bind(('127.0.0.1', 16384))
server.listen(5)
clientList = []

def on_new_client(client,addr):
    clock = pg.time.Clock()
    while True:
        clock.tick(60)
        clientMessage = c.recv(1000).decode()
        print(clientMessage)

        response = '0'
        client.send(response.encode())
    client.close()


run = True
while run:
    (sourceClient, addrClient) = server.accept()
    if sourceClient not in clientList:
        clientList.append((sourceClient, addrClient))
        print('connected clients :',clientList)
        Thread(target=on_new_client,args=(sourceClient, addrClient))

pg.quit()
