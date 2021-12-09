import socket


pred = None
next = None





def send_msg(ip, port, msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(adr['ip'], adr['port'])
    s.send(msg)
    s.close()

     


