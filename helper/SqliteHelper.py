import sqlite3
from sqlite3 import Error
import json


def create_connection(db_path):
    try:
        conn = sqlite3.connect(db_path, check_same_thread=False)
        return conn
    except Error as e:
        print(e)


def execute(conn, sql, params=[]):
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)

        return cursor
    except Error as e:
        print(e, sql, params)


def commit(conn, cursor):
    conn.commit()
    return cursor.lastrowid


def query(conn, sql, params=[]):
    cursor = execute(conn, sql, params)
    return cursor.fetchall()


def query_one(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchone()


def prepare_sql(filters=None, sort='-id', offset=0, limit=20):
    sql = ""
    if filters is not None:
        for field in json.loads(json.dumps(filters)):
            sql = "{} AND {}='{}'".format(sql, field, filters[field])
    if sort is not None:
        sql = "{} ORDER BY {} {}".format(
            sql,
            sort[1:] if sort[0:1] == "-" else sort,
            "DESC" if sort[0:1] == "-" else "ASC"
        )
    if limit is not None:
        sql = "{} LIMIT {}".format(sql, limit)
    if offset is not None:
        sql = "{} OFFSET {}".format(sql, offset)

    return sql
