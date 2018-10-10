import socket, time, json
import os

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
    to = {}
    top['interface'] = os.listdir('/sys/class/net')
    print(top)
    conn.send_mes(json.dumps(top))


