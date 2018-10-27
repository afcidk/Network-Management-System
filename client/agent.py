from scapy.all import *
from connection import Connection
import threading
import func

if __name__ == '__main__': 
    connection = Connection()

    # Sniffing thread
    t1 = threading.Thread(target=lambda: sniff(iface='wlp3s0', prn=func.sniff(connection)), name='sniff')
    t1.start()

    # Wait until thread is done
    t1.join()










