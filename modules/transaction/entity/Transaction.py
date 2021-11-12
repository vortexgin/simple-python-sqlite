import json
import time

from config import conn
from helper.JsonHelper import default
from helper.SqliteHelper import prepare_sql, query, execute, commit, query_one
from modules.user.entity import User


class Transaction:
    __tablename__ = "transactions"

    id = None
    type = None
    amount = None
    actor = None
    recipient = None
    status = None
    created_at = None

    available_fields = ['id', 'type', 'amount', 'actor', 'recipient', 'status', 'created_at']

    TYPE_TOPUP_BALANCE = 'topup'
    TYPE_TRANSFER_IN = 'transferin'
    TYPE_TRANSFER_OUT = 'transferout'

    STATUS_FAILED = 'failed'
    STATUS_PENDING = 'pending'
    STATUS_SETTLED = 'settled'

    def __init__(self, id=None, type=None, amount=None, actor=None, recipient=None, status=None, created_at=None):
        self.id = id
        self.type = type
        self.amount = amount
        self.actor = actor
        self.recipient = recipient
        self.status = status
        self.created_at = int(time.time()) if created_at is None else created_at

    def __str__(self):
        return json.dumps(self.fields(), sort_keys=True, indent=1, default=default, separators=(',', ':'))

    @staticmethod
    def unserialize(row):
        return Transaction(id=row[0], type=row[1], amount=row[2], actor=User().find_by_id(row[3]),
                           recipient=User().find_by_id(row[3]), status=row[5], created_at=row[6])

    @staticmethod
    def after_save(transaction):
        if transaction.status == Transaction.STATUS_FAILED:
            return True

        original_actor_balance = transaction.actor.balance
        original_recipient_balance = transaction.recipient.balance
        try:
            if transaction.type == Transaction.TYPE_TOPUP_BALANCE:
                transaction.recipient.balance = transaction.recipient.balance + transaction.amount
                transaction.recipient.save()
            elif transaction.type == Transaction.TYPE_TRANSFER_IN:
                transaction.recipient.balance = transaction.recipient.balance + transaction.amount
                transaction.recipient.save()
            elif transaction.type == Transaction.TYPE_TRANSFER_OUT:
                transaction.actor.balance = transaction.actor.balance - transaction.amount
                transaction.actor.save()

            if transaction.type == Transaction.TYPE_TRANSFER_OUT:
                transaction_in = Transaction(type=Transaction.TYPE_TRANSFER_IN, amount=transaction.amount,
                                             actor=transaction.actor,
                                             recipient=transaction.recipient, status=Transaction.STATUS_SETTLED)
                transaction_in.save()
        except:
            transaction.actor.balance = original_actor_balance
            transaction.actor.save()
            transaction.recipient.balance = original_recipient_balance
            transaction.recipient.save()
            failed_transaction = Transaction().find_by_id(transaction.id)
            failed_transaction.status = Transaction.STATUS_FAILED
            failed_transaction.save()

    def find_by_id(self, id):
        row = self.find_one(filters={"id": id})

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
            sql = "INSERT INTO {} (type, amount, actor, recipient, status, created_at) VALUES (?, ?, ?, ?, ?, ?)".format(
                self.__tablename__)
            cursor = execute(conn, sql,
                             [self.type, self.amount, self.actor.id, self.recipient.id, self.status, self.created_at])
        else:
            sql = "UPDATE {} SET status=? WHERE id=?".format(self.__tablename__)
            cursor = execute(conn, sql, [self.status, self.id])

        lastrowid = commit(conn, cursor)
        self.id = lastrowid if self.id is None else self.id

        self.after_save(self)

        return self

    def delete(self):
        if self.id is None:
            return False

        sql = "DELETE FROM {} WHERE id=?".format(self.__tablename__)
        execute(conn, sql, [self.id])

        return True

    def get_top_debit_transaction_value(self, limit=10):
        sql = "SELECT users.username, IFNULL((SELECT SUM(amount) FROM {} WHERE type = ? AND actor = users.id AND status = ?), 0) as debit FROM {} GROUP BY users.username ORDER BY debit DESC LIMIT {}".format(self.__tablename__, User.__tablename__, limit)
        return query(conn=conn, sql=sql, params=[Transaction.TYPE_TRANSFER_OUT, Transaction.STATUS_SETTLED])

    def get_top_transaction_per_user(self, limit=10):
        sql = "SELECT users.username, IFNULL((SELECT SUM(amount) FROM {} WHERE type = ? AND actor = users.id AND status = ?), 0) as debit, IFNULL((SELECT SUM(transactions.amount) FROM {} WHERE type IN (?, ?) AND recipient = users.id AND status = ?), 0) as credit FROM {} GROUP BY users.username ORDER BY (debit+credit) DESC LIMIT {}".format(self.__tablename__, self.__tablename__, User.__tablename__, limit)
        return query(conn=conn, sql=sql, params=[Transaction.TYPE_TRANSFER_OUT, Transaction.STATUS_SETTLED, Transaction.TYPE_TRANSFER_IN, Transaction.TYPE_TOPUP_BALANCE, Transaction.STATUS_SETTLED])