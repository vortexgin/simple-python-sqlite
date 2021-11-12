import json
import time
import uuid

from config import conn
from helper.JsonHelper import default
from helper.SqliteHelper import prepare_sql, query, execute, commit, query_one


class User:
    __tablename__ = "users"

    id = None
    username = None
    auth_token = None
    balance = None
    created_at = None

    available_fields = ['id', 'username', 'auth_token', 'balance', 'created_at']

    def __init__(self, id=None, username=None, auth_token=None, balance=None, created_at=None):
        self.id = id
        self.username = username
        self.auth_token = auth_token
        self.balance = balance
        self.created_at = int(time.time()) if created_at is None else created_at

    def __str__(self):
        return json.dumps(self.fields(), sort_keys=True, indent=1, default=default, separators=(',', ':'))

    @staticmethod
    def create_user(username=None):
        return User(username=username, auth_token=str(uuid.uuid4()), balance=0)

    @staticmethod
    def unserialize(row):
        return User(id=row[0], username=row[1], auth_token=row[2], balance=row[3], created_at=row[4])

    def find_by_id(self, id):
        row = self.find_one(filters={"id": id})

        return False if row is None else self.unserialize(row)

    def find_by_username(self, username):
        row = self.find_one(filters={"username": username})

        return False if row is None else self.unserialize(row)

    def find_by_auth_token(self, token):
        row = self.find_one(filters={"auth_token": token})

        return False if row is None else self.unserialize(row)

    def fields(self, excludes=[]):
        return self.__dict__

    def base_query(self, fields):
        return "SELECT {} FROM {} WHERE 1=1".format(fields, self.__tablename__)

    def find(self, filters=None, sort='-id', offset=0, limit=20):
        return query(conn=conn, sql="{}{}".format(self.base_query('*'), prepare_sql(filters, sort, offset, limit)))

    def find_one(self, filters=None, sort='-id'):
        return query_one(conn=conn, sql="{}{}".format(self.base_query('*'), prepare_sql(filters, sort)))

    def save(self):
        if self.id is None:
            sql = "INSERT INTO {} (username, auth_token, balance, created_at) VALUES (?, ?, ?, ?)".format(
                self.__tablename__)
            cursor = execute(conn, sql, [self.username, self.auth_token, self.balance, self.created_at])
        else:
            sql = "UPDATE {} SET balance=? WHERE id=?".format(self.__tablename__)
            cursor = execute(conn, sql, [self.balance, self.id])

        return commit(conn, cursor)