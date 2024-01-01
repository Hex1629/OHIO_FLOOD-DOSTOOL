import sys,threading
input_files = ''
output_files = ''
if len(sys.argv) == 3:
    input_files = sys.argv[1]
    output_files = sys.argv[2]
else:print(f'\x1b[38;5;76m{sys.argv[0]} \x1b[38;5;77m<\x1b[38;5;78mLIST\x1b[38;5;77m> \x1b[38;5;77m<\x1b[38;5;78mOUTPUT-FILE\x1b[38;5;77m>\x1b[0m'); exit()

ip_list = []
def detected(ip,output):
    if ip not in ip_list:
        ip_list.append(ip)
        print(f"\x1b[38;5;76mFound \x1b[38;5;77mIP \x1b[38;5;78m--> \x1b[38;5;79m{ip}\x1b[0m")
        with open(output,'a') as f:
            f.write(f'{ip}\n')
    else:print(f"\x1b[38;5;196mSAME \x1b[38;5;197mIP \x1b[38;5;198m--> \x1b[38;5;226m{ip}\x1b[0m")
th = []
with open(input_files,'r') as f:
    for ip in f.readlines():
        raw = ip.replace('\n','')
        t = threading.Thread(target=detected,args=(raw,output_files))
        t.start()
        th.append(t)
for t in th:
    t.join()