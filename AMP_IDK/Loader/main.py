import socket,sys,time,threading
from generate import Generate_HttpPacket,Generate_ips
from human_format import HumanBytes

# Config anything
Port_Default = 80
Mode_join = 0

# ! Int - DATA
connection = 0
thread = 0
success = 0
failed = 0
exits = 0

# DEF
def http_recv(ip,port,timeout):
 global connection
 data = ''
 try:
  connection += 1
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  if timeout > 0:
   s.settimeout(timeout)
  s.connect((ip,port))
  s.send(Generate_HttpPacket(ip).encode())
  data = s.recv(999999)
 except Exception as e:data = 'Error'
 connection -= 1
 return data

def http_thread(ip,port,timeout):
 global thread,success,failed
 thread += 1
 raw = http_recv(ip,port,timeout)
 if raw != 'Error':
  size = HumanBytes.format(len(raw),True).split(' ')
  with open(size[1]+'_SCANNER.txt','a') as f:
   f.write(f'{ip}\n')
  with open("logs.scan",'a') as f:
   f.write(f'Found --> {ip} SIZE={size[0]} {size[1]} [SUCCESS]\n')
  success += 1
 else:
  failed += 1
 thread -= 1

def Builder(total_output,junk):
 global Mode_join,Port_Default,exits
 th2 = []
 for _ in range(total_output):
  ip = Generate_ips()
  th = threading.Thread(target=http_thread,args=(ip,Port_Default,junk))
  th.start()
  if Mode_join == 1:
   th.join()
  else:th2.append(th)
 if Mode_join == 0:
  for th in th2:
   th.join()
 exits = 1

def output_print(total_output,junk):
 global failed,success,thread,connection,exits
 chara_loaders = ['\\','|','/','-']
 for _ in range(2):
  for a in chara_loaders:
   sys.stdout.write(f"\r \x1b[38;5;226m{time.ctime().split( )[3]} \x1b[38;5;76mLoading \x1b[38;5;77m{a} \x1b[38;5;78m--> \x1b[38;5;79m{total_output}\x1b[0m\033[K")
   sys.stdout.flush()
   time.sleep(0.1)
 threading.Thread(target=Builder,args=(total_output,junk)).start()
 while True:
  data = f'\x1b[38;5;226m{time.ctime().split( )[3]} \x1b[38;5;255m|| \x1b[38;5;196mFailed\x1b[38;5;197m=\x1b[38;5;198m{failed} \x1b[38;5;82mSuccess\x1b[38;5;83m=\x1b[38;5;84m{success} \x1b[38;5;255m|| \x1b[38;5;77mConnect \x1b[38;5;255m- \x1b[38;5;76m{connection} \x1b[38;5;255m|| \x1b[38;5;51mThread \x1b[38;5;255m- \x1b[38;5;50m{thread}\x1b[0m'
  sys.stdout.write(f"\r {data}\x1b[0m\033[K")
  sys.stdout.flush()
  if exits == 1:
   break
 print(f'\n\x1b[38;5;196mFailed\x1b[38;5;197m=\x1b[38;5;198m{failed} \x1b[38;5;82mSuccess\x1b[38;5;83m=\x1b[38;5;84m{success}\x1b[0m')

if len(sys.argv) == 3:
 total_output = int(sys.argv[1])
 timeout = int(sys.argv[2])
else:print(f'\x1b[38;5;76m{sys.argv[0]} \x1b[38;5;77m<\x1b[38;5;78mTOTAL-IP\x1b[38;5;77m> \x1b[38;5;77m<\x1b[38;5;78mTIMEOUT\x1b[38;5;77m>\x1b[0m'); exit()

print(f"\x1b[38;5;76mL\x1b[38;5;77mo\x1b[38;5;78ma\x1b[38;5;79md\x1b[38;5;80me\x1b[38;5;81mr \x1b[38;5;255m- \x1b[38;5;196m{total_output} \x1b[38;5;226m{time.ctime().split( )[3]}\x1b[0m")
with open("logs.scan",'w') as f:
 f.write('Loaders starting . . .\n')
threading.Thread(target=output_print,args=(total_output,timeout)).start()