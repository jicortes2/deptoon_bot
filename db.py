from psycopg2 import connect, IntegrityError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import urllib.parse as urlparse
from constants import DB_NAME, DB_HOST, DB_PASS, DB_PORT, DB_USER

""" table1 = dawg_list (chat int, phrase str)
    table2 = shop (chat int, phrase str) """


def access(option=True):
    """ Returns connection to deptoon database (except when you're
    creating it, on that case returns heroku main database) """
    # urlparse.uses_netloc.append("postgres")
    # url = urlparse.urlparse(os.environ[DATABASE_URL])
    # db = url.path[1:]
    return connect(
                    dbname=DB_NAME,
                    user=DB_USER,
                    password=DB_PASS,
                    host=DB_HOST,
                    port=DB_PORT
                )


def check_db():
    """ Check if deptoon_bot database exists, if it doesn't it is created
    with the necessary tables """
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
    """ Returns true if the thing is added to the table """
    try:
        conn = access()
        cur = conn.cursor()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur.execute("INSERT INTO {} (chat, element) VALUES ({}, '{}')".format(table, chat_id, thing))
        conn.close()
        return True
    except IntegrityError:
        return False


def get_elements(table, chat_id):
    """ Returns the a list with all the elements """
    conn = access()
    cur = conn.cursor()
    cur.execute("SELECT * FROM {} WHERE chat = {}".format(table, chat_id))
    tuples = cur.fetchall()
    conn.close()
    return [i[1] for i in tuples]


def clear_table(table, chat_id):
    """ Delete all the elements of the table related to one chat """
    conn = access()
    cur = conn.cursor()
    cur.execute("DELETE FROM {} WHERE chat = {}".format(table, chat_id))
    conn.close()


# check_db()
