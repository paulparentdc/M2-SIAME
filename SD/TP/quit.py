import threading
import random
import sys
import json
import socket
import logging as log

myPort = None
myId   = None
idUniq = random.randint(0, 1024)

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

    print("Sending ["+ data["type"]+"] to "+str(ip)+":"+str(port))
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
    if(msg["type"] == "ack"):
        print("Ack received")
    
    else:
        print("WTF?")



if len(sys.argv) < 4:
    print("Not enough arguments, call format must be : quit.py [contact_ip] [contact_port] [key]")
    exit()
elif len(sys.argv) == 4:
    dataMsg = {"type":"quit", "key":sys.argv[3], "msgGet":0, "msgPut":0, "msgGest":0}
    send(sys.argv[1], int(sys.argv[2]), dataMsg)
else:
    print("Too many arguments, call format must be : quit.py [contact_ip] [contact_port] [key]")
    exit()
