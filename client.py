from socket import socket

print('starting')
serveur = socket()
serveur.connect( ('192.168.56.1', 16384) )
############

while True:
    reponse = input("> ")
    serveur.send(reponse.encode())

    message = serveur.recv(1000)
    texte = message.decode()
    print(texte)
    if texte == 'end':
        break
    #print(adclient," : \n",donnees.decode(), end='')
    

serveur.close()