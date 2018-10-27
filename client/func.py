import socket, time, json
import os
import parse

# Fault management 1
# Use 53/tcp port to ping 8.8.8.8
def send_internet(conn, host='8.8.8.8', port=53):
    try:
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        conn.send_mes(json.dumps({'internet': True}))
    except Exception as e:
        print(e)
        conn.send_mes(json.dumps({'internet': False}))

# Configuration management 1
# print available interface
def send_config(conn):
    print('here')
    top = {}
    top['interface'] = os.listdir('/sys/class/net')
    print(top)
    conn.send_mes(json.dumps(top))

# Accounting management 1
# send users' usage
def sniff(conn):
    def sniff_callback(pkt):
        parsed = parse.parse_pkt(pkt)
        if parsed is None: return
        else: conn.store_mes(parsed)
    return sniff_callback


