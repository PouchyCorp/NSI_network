from socket import socket

print('starting...')
serveur = socket()
serveur.bind(('192.168.56.1', 16384))
serveur.listen()
(sclient, adclient) = serveur.accept()
if sclient:
    print('connected')

##########
while True:
    message = sclient.recv(1000)
    texte = message.decode()
    print(texte)
    #print(adclient," : \n",donnees.decode(), end='')
    if texte == 'end':
        break

    reponse = input("> ")
    sclient.send(reponse.encode())
    if reponse == 'end':
        break
    
sclient.close()

