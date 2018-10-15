import socket, json, os
import threading
import db, func
from agent import Agent

HOST = '10.0.0.1'
PORT = 5000

def manage_mode():
    global selected_agent
    help_mes = "\
        Usage: (command index)\n\
        +-----+---------------------+\n\
        |index| explanation         |\n\
        +-----+---------------------+\n\
        |  0  | ISOLATE the agent   |\n\
        |  1  | DEISOLATE the agent |\n\
        +-----+---------------------+\n\
        |quit | leave manage mode   |\n\
        +-----+---------------------+\n\
    "
    print(help_mes)
    manage_funcs = [func.isolate, func.deisolate]
    while True:
        s = input('(Manage mode) ')
        if s == 'quit':
            break
        elif s.isdigit():
            manage_funcs[int(s[0])](list(selected_agent.keys())[0])
        else:
            print(help_mes)

def plot_mode():
    help_mes = "\
        Usage: (command index) (agent_ip)\n\
        +--------+------------------------+\n\
        |commands| explanation            |\n\
        +--------+------------------------+\n\
        | help   | Show plot option       |\n\
        | quit   | Leave plot mode        |\n\
        +-----+--+---------------------------------------+\n\
        |index| explanation                              |\n\
        +-----+------------------------------------------+\n\
        |  0  | Total traffic size                       |\n\
        |  1  | Traffic size separated by time intervals |\n\
        |  2  | Traffic size sorted by applications      |\n\
        +-----+------------------------------------------+\n\
    "
    plot_funcs = [func.plot_bar, None, None]

    print(help_mes)
    while True:
        s = input('(Plot mode) ')
        if s == 'quit':
            break
        elif s == 'help':
            print(help_mes)
        else:
            s = s.split()
            if len(s) == 2 and s[0].isdigit():
                plot_funcs[int(s[0])](s[1])
            else:
                print(help_mes)

def input_thread():
    global selected_agent
    help_mes = "\
        +---------------------------------+\n\
        |commands| explanation            |\n\
        +--------+------------------------+\n\
        | list   | List available agents  |\n\
        | select | Select an agent        |\n\
        | manage | Manage selected agent  |\n\
        | help   | Show help message      |\n\
        | quit   | Leave program          |\n\
        | plot   | Enter plot mode        |\n\
        +---------------------------------+\n\
    "

    states = []
    while True:
        s = input('[{}] '.format(list(selected_agent.keys())[0]))
        if s=='list':
            print("Available agents:")
            print(' '.join(s for s in agent_list.keys()))
            states = []
        elif 'select' in s:
            tl = s.split(' ')
            if len(tl) != 2:
                print("Usage: select [IP]")
            else:
                s = tl[1]
                try:
                    selected_agent = {s:agent_list[s]}
                    print("Select success")
                    states = ['wait_for_command']
                except KeyError:
                    print("Agent not in list, enter again")
        elif 'plot' in s:
            plot_mode()
        elif 'manage' in s:
            manage_mode()
        elif s=='help':
            print(help_mes)
        elif s=='quit':
            print("Bye~")
            os._exit(0)
        elif 'wait_for_command' in states:
            agent_tmp = list(selected_agent.values())[0]
            if agent_tmp == None: continue

            try:
                agent_tmp.send_mes(s+'\n')
            except BrokenPipeError as e:
                pass
        else:
            print(help_mes)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)

agent_list = {}
selected_agent = {'None':None}

ithread = threading.Thread(target=input_thread)
ithread.start()


while True:
    conn, addr = s.accept()
    agent = Agent(conn, addr)
    if len(agent_list) == 0: # auto select
        print('[+] Agent {} Connected\n[{}] '.format(addr, addr[0]))
        agent_list.update({addr[0]:agent})
        selected_agent = {addr[0]:agent}
    else:
        if addr[0] in agent_list.keys():
            selected_agent = {addr[0]:agent}
            print('[!] Agent {} Resetted'.format(addr))
        else:
            agent_list.update({addr[0]:agent})
            print('[+] Agent {} Connected'.format(addr))

    while True:
        try:
            data = conn.recv(1024).decode()
        except ConnectionResetError:
            print("Connection Resetted")
            selected_agent = {'None': None}

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
