from psycopg2 import connect, IntegrityError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import urlparse


def access(option=True):
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    db = 'deptoon_bot' if option else url.path[1:]
    return connect(
                    dbname=db,
                    user=url.username,
                    password=url.password,
                    host=url.hostname,
                    port=url.port
                )


def check_db():
    conn = access(option=False)
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
        conn = access()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        tables = ['dawg_list', 'shop']
        for table in tables:
            print("CREATE TABLE {} (chat int,phrase varchar(200) PRIMARY KEY)".format(table))
            cur.execute("CREATE TABLE {} (chat int, element varchar(200) PRIMARY KEY)".format(table))
        conn.close()


def add_element(table, chat_id, thing):
    try:
        conn = access()
        cur = conn.cursor()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur.execute("INSERT INTO {} (chat, element) VALUES ({}, '{}')".format(table, chat_id, thing))
        conn.close()
        return True
    except IntegrityError:
        return False


def get_elements(table):
    conn = access()
    cur = conn.cursor()
    cur.execute("SELECT * FROM {}".format(table))
    tuples = cur.fetchall()
    conn.close()
    return [i[1] for i in tuples]


def clear_table(table, chat_id):
    conn = access()
    cur = conn.cursor()
    cur.execute("DELETE FROM {} WHERE chat = {}".format(table, chat_id))
    conn.close()


check_db()
