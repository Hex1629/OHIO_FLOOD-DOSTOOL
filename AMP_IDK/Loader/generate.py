import random,string

def Generate_HttpPacket(ip):
    method = 'GET' # config type methods
    path = '/' # config path
    end = '\n\n\r\r' # config end
    return '%s %s HTTP/1.1\nHost: %s%s'%(method,path,ip,end)

def Generate_ips():
    ip = [str(random.randint(0, 255)) for _ in range(4)]
    return '.'.join(ip)