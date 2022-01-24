import threading
import random
import sys
import json
import socket
import logging as log
import time

SYSTEM_SIZE = 32
BUFFER_SIZE = 2048

#Variables du noeud
myIP     = None
myPort   = None
myKey    = None
myNeigh  = {}       #table de voisinnage au format {clé:[key, ip, port], ...}
myData   = {}       #données des key dont il est responsable

nbMsgGet = 0
nbMsgPut = 0
nbMsgGes = 0

amIFirst   = False
amIAlone   = False
amILeaving = False

contactIp   = None
contactPort = None

#-----------------------------------------------------------------------------------------------
#-------------------------------------Fonctions utilitaires-------------------------------------
def affiche(msg):
    print("Noeud "+str(myKey)+" : "+str(msg))


def firstNode(port):
    global myIp, myPort, myKey, amIFirst, myNeigh, amIAlone
    myIp            = socket.gethostbyname(socket.gethostname())
    myPort          = port
    myKey           = random.randint(0, SYSTEM_SIZE-1)
    amIFirst        = True
    amIAlone        = True
    myNeigh["pred"] = [myKey, myIp, myPort]
    myNeigh["next"] = [myKey, myIp, myPort]

    affiche("created with ["+str(myIp)+":"+str(myPort)+"] !")
    printNeigh()


def newNode(port, cIp, cPort):
    global myIp, myPort, myKey, amIFirst, myNeigh, contactIp, contactPort
    myIp        = socket.gethostbyname(socket.gethostname())
    myPort      = port
    contactIp   = cIp
    contactPort = cPort
    
    affiche("created with ["+str(myIp)+":"+str(myPort)+"] !")
    tryToJoin(cIp, cPort)
    

def tryToJoin(contactIp, contactPort):
    global nbMsgGes
    affiche("trying to join")
    trialKey = random.randint(0, SYSTEM_SIZE-1)
    dataMsg = {"type":"join", "key":trialKey, "ip":myIp, "port":myPort}
    nbMsgGes = nbMsgGes + 1 
    send(contactIp, contactPort, dataMsg)


def amIResp(key):#retourne True si l'on est responsable du noeud en paramètre
    keyPred = myNeigh['pred'][0]

    if key == myKey:
        return True
    elif amIAlone == True:
        return True
    elif keyPred <= myKey:#Cas normal
        if key > keyPred:
            return True

    elif keyPred >= myKey:#Cas "à cheval" sur la boucle
        if key > keyPred or key <= myKey:
            return True

    return False


def makeInit(key, ip, port):#gère la création des données pour un nouveau noeud
    global myNeigh, nbMsgGes
    #Récupération des datas
    nodeData  = {}
    for k, v in myData.items():
        if myKey > key:#Cas normal
            if k <= key or k > myKey:
                nodeData[k] = v
        else:#Cas "à cheval" sur la boucle
            if k <= key and k > myKey:
                nodeData[k] = v

    

    #Envoi de l'INIT
    nodeNeigh = {"next":[myKey, myIp, myPort], "pred":myNeigh["pred"]}

    #Màj de la table de voisinnage
    myNeigh["pred"] = [key, ip, port]

    data = {"type":"init", "key":key, "data":nodeData, "tv":nodeNeigh}
    nbMsgGes = nbMsgGes + 1
    send(ip, port, data)


def printNeigh():
    print("My neighbours are : ")
    print("  pred : "+str(myNeigh["pred"][0]))
    print("  next : "+str(myNeigh["next"][0]))
    print(" ")


def printData():
    print("My datas are : ")
    for n, d in myData:
        print(str(n)+" : "+str(str(d)))


def updateNeighbours(key, ip, port):
    pred = myNeigh["pred"]
    next = myNeigh["next"]

    if key > myKey:
        if key<next[0]:
            myNeigh["next"] = [key, ip, port]
        elif next[0]<=myKey:
            myNeigh["next"] = [key, ip, port]
        elif pred[0]>=myKey and key>pred[0]:
            myNeigh["pred"] = [key, ip, port]
    elif key < myKey:
        if key>pred[0]:
            myNeigh["pred"] = [key, ip, port]
        elif pred[0]>=myKey:
            myNeigh["pred"] = [key, ip, port]
        elif next[0]<=myKey and key<next[0]:
            myNeigh["next"] = [key, ip, port]


#-----------------------------------------------------------------------------------------------
#-------------------------------Fonctions de gestion des messages-------------------------------


def put(key, val, idUniq, ip, port):
    global nbMsgPut
    nbMsgPut = nbMsgPut + 1
    if amIResp(key):
        #Màj des data
        myData[key] = val
        affiche("data update : "+str(myData))
        #Envoi de l'ACK
        #dataMsg = {"type":"ack", "ok":"ok", "idUniq":idUniq}
        #send(ip, port, dataMsg)
    else:
        #Transmission au prédécesseur
        dataMsg = {"type":"put", "key":key, "val":val, "idUniq":idUniq, "ip":ip, "port":port}
        send(myNeigh["pred"][1], myNeigh["pred"][2], dataMsg) 


def get(key, ip, port):
    global nbMsgGet
    nbMsgGet = nbMsgGet + 1
    if amIResp(key):
        if key in myData:
            dataMsg = {"type":"answer", "key":key, "val":myData[key]}
        else:
            dataMsg = {"type":"answer", "key":key, "val":None}
        send(ip, port, dataMsg)
    else:
        dataMsg = {"type":"get", "key":key, "ip":ip, "port":port}
        send(myNeigh["pred"][1], myNeigh["pred"][2], dataMsg) 


def join(key, ip, port):
    global nbMsgGes
    affiche("node "+str(key)+" is trying to join")
    if amIResp(key):
        if key == myKey:
            dataMsg = {"type":"reject", "key":key}
            nbMsgGes = nbMsgGes + 1
            send(ip, port, dataMsg) #refus
        else:
            amIAlone = False
            makeInit(key, ip, port)
            
    else:
        affiche("not resp")
        #Transmission au prédécesseur
        dataMsg = {"type":"join", "key":key, "ip":ip, "port":port}
        nbMsgGes = nbMsgGes + 1
        send(myNeigh["pred"][1], myNeigh["pred"][2], dataMsg) 


def init(key, data, tv):
    global myKey, myData, myNeigh, nbMsgGes
    myKey   = key
    myData  = data
    myNeigh = tv
    affiche("------INIT------")
    printNeigh()
    printData()
    dataMsg = {"type":"new", "key":myKey, "ip":myIp, "port":myPort}
    nbMsgGes = nbMsgGes + 1
    send(myNeigh["pred"][1], myNeigh["pred"][2], dataMsg)
    


def quit(key, msgGet, msgPut, msgGest):
    global amILeaving
    if amILeaving:
        affiche("Everybody left :")
        affiche("     get    -> "+str(msgGet))
        affiche("     put    -> "+str(msgPut))
        affiche("     others -> "+str(msgGest))
        exit()
    else:
        dataMsg = {"type":"quit", "key":key, "msgGet":msgGet+nbMsgGet, "msgPut":msgPut+nbMsgPut, "msgGest":msgGest+nbMsgGes+1}
        send(myNeigh["pred"][1], myNeigh["pred"][2], dataMsg)
        if msgGest == 0:
            amILeaving = True
        else:
            exit()
    


def new(key, ip, port):
    global nbMsgGes
    if key != myKey:
        updateNeighbours(key, ip, port)
        dataMsg = {"type":"new", "key":key, "ip":ip, "port":port}
        printNeigh()
        nbMsgGes = nbMsgGes + 1 
        send(myNeigh["pred"][1], myNeigh["pred"][2], dataMsg)
    else:
        affiche("NEW has been received by everyone")


def reject(key):
    affiche("received REJECT")
    tryToJoin(contactIp, contactPort)


def messageHandler(msg):
    time.sleep(1)
    type = msg["type"]
    affiche("["+type+"] received : "+str(msg))
    if type == "join":
        join(msg["key"], msg["ip"], msg["port"])
    elif type == "reject":
        reject(msg["key"])
    elif type == "put":
        put(msg["key"], msg["val"], msg["idUniq"], msg["ip"], msg["port"])
    elif type == "new":
        new(msg["key"], msg["ip"], msg["port"])
    elif type == "get":
        get(msg["key"], msg["ip"], msg["port"])
    elif type == "init":
        init(msg["key"], msg["data"], msg["tv"])
    elif type == "quit":
        quit(msg["key"], msg["msgGet"], msg["msgPut"], msg["msgGest"])
    else:
        pass


#-----------------------------------------------------------------------------------------------
#----------------------------------Fonctions de communication-----------------------------------

def send(ip, port, data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #affiche("sending ["+ data["type"]+"] to "+str(ip)+":"+str(port))
    
    try:
        s.connect((ip, port))
    except socket.error as e:
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((ip, port))
        except socket.error as e:
            s.close()
            #affiche("impossible to connect")
            send(ip, port, data)
            return

    affiche("sending ["+ data["type"]+"] to "+str(ip)+":"+str(port))
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
    try:
        msg = json.loads(rec)
    except Exception as e:
        print("Error while loading")
        return
    messageHandler(msg)


#-----------------------------------------------------------------------------------------------
#----------------------------------------------MAIN---------------------------------------------

if len(sys.argv) <= 1:
    print("Not enough arguments, call format must be : noeud.py self_port [contact_ip] [contact_port]")
    exit()
elif len(sys.argv) == 2:
    firstNode(int(sys.argv[1]))
elif  len(sys.argv) == 4:
    newNode(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]))
else:
    print("Wrong number of arguments, call format must be : noeud.pyself_port [contact_ip] [contact_port]")
    exit()

while(True):
    receive()