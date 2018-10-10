import pymysql

db = pymysql.connect('localhost', 'root', '', 'netflow')

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
        print("error: " + str(e))
        db.rollback()

def get_ip_sorted():
    try:
        cur.execute("select src, dst from flows")
        data = cur.fetchOne()
        print(data)
    except Exception as e:
        print("error: " + str(e))

