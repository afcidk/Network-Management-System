import threading, time
import db

class Agent():
    def __init__(self, conn, addr):
        self.pool = {}
        self.conn = conn
        self.addr = addr
        self.rthread = threading.Thread(target=self.refresh_thread, name='refresh_thread')
        self.rthread.start()

    def send_mes(self, msg):
        self.conn.send((msg+'\n').encode())
        print("sent {}".format(msg))

    def add_pkt(self, pkt):
        src = pkt['src']
        dst = pkt['dst']
        typ = pkt['type']
        l = pkt['len']
        
        tup = (src, dst)
        if tup in self.pool:
            tar = self.pool[tup]
            if typ in tar:
                tar[typ] += l
            else:
                tar[typ] = l
        else:
            self.pool[tup] = {typ: l}

    def refresh_thread(self):
        print("Refresh Thread started")
        while True:
            try:
                for x in self.pool.keys():
                    src = x[0]
                    dst = x[1]
                    for t in self.pool[x].keys():
                        typ = t
                        l = self.pool[x][t]

                        print(src, dst, typ, l)
                        db.add_flow(src, dst, l, typ)
                self.pool = {}
            except Exception as e:
                print(e)
                continue
            # Refresh every 1 minutes
            time.sleep(1*60)

