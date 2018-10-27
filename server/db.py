import pymysql

db = pymysql.connect('localhost', 'root', '', 'NMS')

cur = db.cursor()

def add_flow(src, dst, l, typ):
    try:
        cur.execute("select len from flows where src='{}' and dst='{}'".format(src, dst))
        prev_len = cur.fetchone()

        if prev_len is None:
            cur.execute("insert into flows (src, dst, len, type) values('{}', '{}', '{}', '{}')".format(src, dst, l, typ))
        else:
            cur.execute("update flows set len='{}' where src='{}' and dst='{}'".format(prev_len[0]+l, src, dst))

        db.commit()
        print("success: ", end='')
        print(src, dst, l, typ)

    except Exception as e:
        print("error in add_flow: " + str(e))
        db.rollback()

def get_ip_sorted():
    try:
        cur.execute("select src, dst from flows")
        data = cur.fetchOne()
        print(data)
    except Exception as e:
        print("error in get_ip_sorted: " + str(e))

def get_flow_size(target, origin):
    if origin=='src':
        end = 'dst'
    else:
        end = 'src'

    try:
        cur.execute("select {0},{1} from flows where {2}='{3}' and {0}!='10.0.0.1'".format(end, 'len', origin, target))
        return list(cur.fetchall())
    except Exception as e:
        print("error in get_flow_size: "+str(e))
        return None

def get_agent_up_time(agent):
    cur.execute("select TIME_TO_SEC(time), isup from agent where agent='{}' order by time desc;".format(agent))
    result = cur.fetchall()
    if len(result) <= 0: return ()

    if result[0][1] == 1:
        set_agent_time(agent, 0) # set temporary down

    cur.execute("select TIME_TO_SEC(time), isup from agent where agent='{}' order by time desc;".format(agent))
    result = cur.fetchall()
    set_agent_time(agent, 1) # set up again
    print(result)

    ret = []
    up_time = []
    down_time = []
    for res in result:
        if res[1] == 0: down_time.append(res[0])
        else: up_time.append(res[0])

    for tb, ta in zip(up_time, down_time):
        ret.append((tb, ta-tb))

    least_time = min(ret, key=lambda x: x[0])[0]
    ret = [(s[0]-least_time, s[1]) for s in ret]
    return ret


def set_agent_time(agent, isUp):
    try:
        cur.execute("insert into agent (agent, isUp) values('{}', '{}')".format(agent, isUp))
        db.commit()
    except Exception as e:
        print("set_agent_time: {}".format(e))
