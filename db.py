from psycopg2 import connect, IntegrityError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def check_db():
    conn = connect(dbname="postgres", password='juan5826', host='localhost')
    cur = conn.cursor()
    cur.execute("SELECT 1 from pg_database WHERE datname='deptoon_bot'")
    tupla = cur.fetchone()
    try:
        if tupla[0]:
            conn.close()
            print('Ya existe la DB, puedes continuar sin problemas')
    except TypeError:
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur.execute("CREATE DATABASE deptoon_bot")
        conn.close()
        conn = connect(dbname="deptoon_bot", password="juan5826")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        tables = ['dawg_list', 'shop']
        for table in tables:
            print("CREATE TABLE {} (chat int,phrase varchar(200) PRIMARY KEY)".format(table))
            cur.execute("CREATE TABLE {} (chat int, element varchar(200) PRIMARY KEY)".format(table))
        conn.close()


def add_element(table, chat_id, thing):
    try:
        conn = connect(dbname="deptoon_bot", password='juan5826')
        cur = conn.cursor()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur.execute("INSERT INTO {} (chat, element) VALUES ({}, '{}')".format(table, chat_id, thing))
        conn.close()
        return True
    except IntegrityError:
        return False


def get_elements(table):
    conn = connect(dbname="deptoon_bot", password='juan5826')
    cur = conn.cursor()
    cur.execute("SELECT * FROM {}".format(table))
    tuples = cur.fetchall()
    conn.close()
    return [i[1] for i in tuples]



def clear_table(table, chat_id):
    conn = connect(dbname="postgres", password='juan5826')
    cur = conn.cursor()
    cur.execute("DELETE FROM {} WHERE chat = {}".format(table, chat_id))
    conn.close()


check_db()
for i, el in enumerate(['a','safdsa', 'sdfasdf']):
    add_element('dawg_list', i, el)
print(get_elements('dawg_list'))
