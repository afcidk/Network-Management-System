PROTOCOL_TYPES = ['ARP', 'TCP', 'UDP', 'ICMP']

def parse_pkt(pkt):
    # Parse IP only now
    ret = {}
    for t in PROTOCOL_TYPES:
        if t in pkt:
            ret['type'] = t
    if 'IP' in pkt:
        pkt = pkt['IP']
        ret['len'] = pkt.len
        ret['src'] = pkt.src
        ret['dst'] = pkt.dst
        return {'packet': ret}

    else: return None

    '''
    top = {} 
    ret = {}
    ret['src'] = pkt.src 
    ret['dst'] = pkt.dst 
    try:
        ret['len'] = pkt.len
    except:
        print(pkt)
    ret['type'] = 'Other'
    for t in PROTOCOL_TYPES:
        if t in pkt:
            ret['type'] = t
    top['packet'] = ret

    return top
    '''
