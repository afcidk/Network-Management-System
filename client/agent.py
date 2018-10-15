from scapy.all import *
from config import HOST, PORT
import func, parse
import threading, time, json, time
import socket

class Connection():
    def __init__(self):
        self.trying_to_connect = False
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

        self.start_connection()

        t1.start()
        t2.start()
        t3.start()

    def start_connection(self):
        if not self.trying_to_connect:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.trying_to_connect = True
            while True:
                try:
                    self.s.connect((HOST, PORT))
                    print("[+] Connected to Server")
                    self.trying_to_connect = False
                    break
                except Exception as e: 
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
            print("Waiting for input")
            try:
                cmd = self.s.recv(1024).decode().split()[0]
                print("Received: {}".format(cmd))
                if cmd == 'config':
                    func.send_config(self)
                elif cmd == 'internet':
                    func.send_internet(self)
                else:
                    self.send_mes(json.dumps({"Error": "Unknown command"}))
            except IndexError as e:
                self.start_connection()
            except OSError as e:
                print(e)

    def fault_thread(self):
        top = {}
        while True:
            func.send_internet(self)
            time.sleep(10)

    def send_mes(self, st):
        try:
            print('sending...  ' + st)
            self.s.send((st+'\n').encode())
        except BrokenPipeError:
            print("[!] Broken Pipe")
            self.start_connection()

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
