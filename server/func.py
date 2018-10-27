import matplotlib.pyplot as plt
import numpy as np
import os
import db

def plot_bar():
    agent = input('Enter agent, q to quit(q):')
    if agent == '\n' or agent == 'q':
        return 

    data = db.get_flow_size(agent, 'src')
    print(data)

    ips = [x[0] for x in data]
    sizes = tuple(np.array([x[1]/1024 for x in data]))

    fig, ax = plt.subplots()
    y_pos = np.arange(len(ips))

    ax.barh(y_pos, width=sizes, align='center', color='green')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(ips)
    ax.invert_yaxis()
    ax.set_xlabel('Size (KB)')
    ax.set_title('Traffic size from agent {}'.format(agent))
    
    plt.show(block=False)

def isolate(agent):
    os.system("sudo iptables -I FORWARD -s {} -j REJECT".format(agent))
def deisolate(agent):
    os.system("sudo iptables -D FORWARD -s {} -j REJECT".format(agent))

def agent_up_time():
    try:
        with open('target_list.txt', 'r') as f:
            targets = [t.split()[0] for t in f.readlines()]
    except FileNotFoundError as e:
        print(e)

    fig, ax = plt.subplots()
    cnt = 0
    color = ['green', 'black', 'blue', 'red', 'gray', 'yellow']
    inter = 4
    height = 16
    for target in targets:
        # in [(a,b), (c,d), (e,f)] format
        intervals = db.get_agent_up_time(target)
        if len(intervals) <= 0: continue

        ax.broken_barh(intervals, (cnt*(inter+height), height), facecolors=color[cnt%6])
        cnt += 1

    ax.set_yticks(range(inter+int(height/2), (height+inter)*len(targets), (height+inter)))
    ax.set_yticklabels(targets)
    plt.show()
