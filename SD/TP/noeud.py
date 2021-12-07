import threading
import random
import sys
import json
import socket
import logging as log

SYSTEM_SIZE = 32
BUFFER_SIZE = 2048

#Variables du noeud
myIP     = None
myPort   = None
myKey    = None
myNeigh  = {}       #table de voisinnage au format {clé:[key, ip, port], ...}
myData   = {}

amIFirst = False

contactIp   = None
contactPort = None

#-----------------------------------------------------------------------------------------------
#-------------------------------------Fonctions utilitaires-------------------------------------
def affiche(msg):
    print("Noeud "+str(myKey)+" : "+msg)


def firstNode(port):
    global myIp, myPort, myKey, amIFirst, myNeigh
    myIp            = socket.gethostbyname(socket.gethostname())
    myPort          = port
    myKey           = random.randint(0, SYSTEM_SIZE-1)
    amIFirst        = True
    myNeigh["pred"] = [myKey, myIp, myPort]
    myNeigh["next"] = [myKey, myIp, myPort]

    affiche("created with ["+str(myIp)+":"+str(myPort)+"] !")


def newNode(port, cIp, cPort):
    global myIp, myPort, myKey, amIFirst, myNeigh, contactIp, contactPort
    myIp        = socket.gethostbyname(socket.gethostname())
    myPort      = port
    contactIp   = cIp
    contactPort = cPort
    
    tryToJoin(cIp, cPort)
    

def tryToJoin(contactIp, contactPort):
    affiche("trying to join")
    trialKey = random.randint(0, SYSTEM_SIZE-1)
    dataMsg = {"type":"join", "key":trialKey, "ip":myIp, "port":myPort}
    affiche("sending "+str(dataMsg))
    send(contactIp, contactPort, dataMsg)


def amIResp(key):#retourne True si l'on est responsable du noeud en paramètre
    keyPred = myNeigh["pred"][0]

    if key == myKey:
        return True

    elif keyPred <= myKey:#Cas normal
        if key >= keyPred:
            return True

    elif keyPred >= myKey:#Cas "à cheval" sur la boucle
        if key >= keyPred or key <= myKey:
            return True

    return False


def makeInit(key, ip, port):#gère la création des données pour un nouveau noeud
    #Récupération des datas
    nodeData  = {}
    for k, v in myData.items():
        if myKey > key:#Cas normal
            if k <= key or k > myKey:
                nodeData[k] = v
        else:#Cas "à cheval" sur la boucle
            if k <= key and k > myKey:
                nodeData[k] = v

    #Màj de la table de voisinnage
    myNeigh["pred"] = [key, ip, port]

    #Envoi de l'INIT
    nodeNeigh = {"next":[myKey, myIp, myPort], "pred":myNeigh["pred"]}
    data = {"type":"init", "key":key, "data":nodeData, "tv":nodeNeigh}
    send(ip, port, data)


#-----------------------------------------------------------------------------------------------
#-------------------------------Fonctions de gestion des messages-------------------------------


def put(key, val, idUniq, ip, port):
    if amIResp(key):
        #Màj des data
        myData[key] = val

        #Envoi de l'ACK
        dataMsg = {"type":"ack", "ok":"ok", "idUniq":idUniq}
        send(ip, port, dataMsg)
    else:
        #Transmission au prédécesseur
        dataMsg = {"type":"put", "key":key, "val":val, "idUniq":idUniq, "ip":ip, "port":port}
        send(myNeigh["pred"][1], myNeigh["pred"][2], dataMsg) 


def get(key, ip, port):
    if amIResp(key):
        if myData.has_key(key):
            dataMsg = {"type":"answer", "key":key, "val":myData[key]}
        else:
            dataMsg = {"type":"answer", "key":key, "val":None}
        send(ip, port, dataMsg)
    else:
        dataMsg = {"type":"get", "key":key, "ip":ip, "port":port}
        send(myNeigh["pred"][1], myNeigh["pred"][2], dataMsg) 


def join(key, ip, port):
    affiche("node "+str(key)+" is trying to join")
    if amIResp(key):
        if key == myKey:
            dataMsg = {"type":"reject", "key":key}
            send(ip, port, dataMsg) #refus
        else:
            makeInit(key, ip, port)
            
    else:
        #Transmission au prédécesseur
        dataMsg = {"type":"join", "key":key, "ip":ip, "port":port}
        send(myNeigh["pred"][1], myNeigh["pred"][2], dataMsg) 


def init(key, data, tv):
    myKey   = key
    myData  = data
    myNeigh = tv
    affiche("received INIT")


def quit(key, msgGet, msgPut, mg):
    pass


def new(key, ip, port):
    if key != myKey:
        dataMsg = {"type":"new", "key":key, "ip":ip, "port":port}
        send(myNeigh["pred"][1], myNeigh["pred"][2], dataMsg)
    else:
        affiche("NEW has been received by everyone")


def reject(key):
    affiche("received REJECT")
    tryToJoin(contactIp, contactPort)


def messageHandler(msg):
    print("yo")
    type = msg["type"]
    if type == "join":
        join(msg["key"], msg["ip"], msg["port"])
    elif type == "put":
        put(msg["key"], msg["val"], msg["idUniq"], msg["ip"], msg["port"])
    elif type == "new":
        new(msg["key"], msg["ip"], msg["port"])
    elif type == "get":
        get(msg["key"], msg["ip"], msg["port"])
    else:
        pass


#-----------------------------------------------------------------------------------------------
#----------------------------------Fonctions de communication-----------------------------------

def send(ip, port, data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    affiche("sending to "+str(ip)+":"+str(port))
    s.connect((ip, port))
    s.send(bytes(json.dumps(data), "utf-8"))
    s.close()


def receive():
    s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(('', myPort))
    except socket.error as e:
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', myPort))
        except socket.error as e:
            s.close()
            print("Error while connecting to port")
            return
    s.listen(2)
    
    client, addr = s.accept()
    
    rec = ''
    allReceived = False
    try:
        while(not allReceived):
            incomingData = client.recv(BUFFER_SIZE).decode()
            if(incomingData == ''):
                allReceived = True
            else:
                rec += incomingData
    except socket.error as e:
        print("Error while receiving")
        s.close()
        return
    print(rec)
    try:
        msg = json.loads(rec)
    except Exception as e:
        print("Error while loading")
        return
    print("yoyo")
    messageHandler(msg)


#-----------------------------------------------------------------------------------------------
#----------------------------------------------MAIN---------------------------------------------

if len(sys.argv) <= 1:
    print("Not enough arguments, call format must be : noeud.py self_port [contact_ip] [contact_port]")
elif len(sys.argv) == 2:
    firstNode(int(sys.argv[1]))
elif  len(sys.argv) == 4:
    newNode(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]))
else:
    print("Wrong number of arguments, call format must be : noeud.pyself_port [contact_ip] [contact_port]")

while(True):
    receive()