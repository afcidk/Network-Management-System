from scapy.all import *
from config import HOST, PORT
import func, parse
import threading, time, json, time
import socket

class Connection():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mes = []

        # Send message thread
        t1 = threading.Thread(target=self.send_mes_thread,
                name='send_thread')

        # Command input thread
        t2 = threading.Thread(target=self.input_thread,
                name='input_thread')

        # Fault thread
        t3 = threading.Thread(target=self.fault_thread,
                name='fault_thread')

        while True:
            try:
                self.s.connect((HOST, PORT))
                t1.start()
                t2.start()
                t3.start()
                break
            except: 
                print("[!] Connecting to server...")
                time.sleep(1)

    def store_mes(self, parsed):
        self.mes.append(parsed)

    def send_mes_thread(self):
        while True:
            for p in self.mes:
                print("sending {}".format(json.dumps(p)))
                self.send_mes(json.dumps(p))                
            self.mes = []
            # send message every 3 minutes
            time.sleep(3*60)
    def input_thread(self):
        while True:
            cmd = self.s.recv(1024).decode().split()[0]
            if cmd == 'config':
                func.send_config(self)
            elif cmd == 'internet':
                func.send_internet(self)
    def fault_thread(self):
        top = {}
        while True:
            func.send_internet(self)
            time.sleep(10)

    def send_mes(self, st):
        try:
            self.s.send((st+'\n').encode())
        except BrokenPipeError:
            print("[!] Broken Pipe")
            self.__init__()

def sniff_callback(pkt):
    parsed = parse.parse_pkt(pkt)
    if parsed is None: return
    else: connection.store_mes(parsed)


connection = Connection()

# Sniffing thread
t1 = threading.Thread(target=lambda: sniff(iface='wlp3s0', prn=sniff_callback), name='sniff')
t1.start()

# Wait until thread is done
t1.join()
t2.join()
t3.join()
