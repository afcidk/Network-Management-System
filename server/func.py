import matplotlib.pyplot as plt
import numpy as np
import os
import db

def plot_bar(agent):

    data = db.get_flow_size(agent, 'src')

    ips = [x[0] for x in data]
    sizes = tuple(np.array([x[1]/1024 for x in data]))
    print(sizes)

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
    
