

import psycopg2


def test():
    conn = None
    try:
        conn = psycopg2.connect(host="192.168.0.109",database="test_cmdb", user="jan", password="kee5daij")
        cur = conn.cursor()
        com =  create_table()
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def conn():
    c = psycopg2.connect(host="192.168.0.109",database="test_cmdb", user="jan", password="kee5daij")
    return c

def cur(conn):
    return conn.cursor()

def run_statement(sql):
    conn = None
    try:
        conn = psycopg2.connect(host="192.168.0.109",database="test_cmdb", user="jan", password="kee5daij")
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def commit(conn):
    conn.commit()

def close_conn(conn):
    conn.close()

def vendors_table():
    command = (
        '''
        CREATE TABLE vendors (
            vendor_id SERIAL PRIMARY KEY,
            vendor_name VARCHAR(255) NOT NULL
        )
        '''
    )
    return command

def drop_table(tname):
    sql = 'DROP TABLE IF EXISTS {};'.format(tname)
    return sql

def insert_vendor_list(vendor_list):
    """ insert a new vendor into the vendors table """
    sql = "INSERT INTO vendors(vendor_name) VALUES(%s)"
    conn = None
    try:
        conn = psycopg2.connect(host="192.168.0.109",database="test_cmdb", user="jan", password="kee5daij")
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(sql,vendor_list)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_vendors():
    """ query data from the vendors table """
    conn = None
    try:
        #params = config()
        conn = psycopg2.connect(host="192.168.0.109",database="test_cmdb", user="jan", password="kee5daij")
        cur = conn.cursor()
        cur.execute("SELECT vendor_id, vendor_name FROM vendors ORDER BY vendor_name")
        print("The number of parts: ", cur.rowcount)
        row = cur.fetchone()
 
        while row is not None:
            print(row)
            row = cur.fetchone()
 
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def delete_entry(v_id):
    rows_deleted = 0
    sql = 'DELETE FROM vendors WHERE vendor_id = %s;'
    c = conn()
    cu = cur(c)
    cu.execute(sql, (v_id,))
    rows_deleted = cu.rowcount
    c.commit()
    cu.close()
    return rows_deleted

if __name__ == '__main__':
    # conn = conn()
    # cur = cur(conn)
    # com = vendors_table()
    # run_statemeent(cur, com)
    # commit(conn)
    # close_conn(conn)
    
    #drop tables
    #sql = drop_table('vendors')
    #run_statement(sql)


    #create table
    # sql = vendors_table()
    # run_statement(sql)

    #insert
    # insert_vendor_list([
    #     ('AKM Semiconductor Inc.',),
    #     ('Asahi Glass Co Ltd.',),
    #     ('Daikin Industries Ltd.',),
    #     ('Dynacast International Inc.',),
    #     ('Foster Electric Co. Ltd.',),
    #     ('Murata Manufacturing Co. Ltd.',)
    # ])

    #delete
    for i in range(1,6):
        print(delete_entry(i))


    get_vendors()



