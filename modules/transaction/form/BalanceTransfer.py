from marshmallow import Schema, fields, validates, ValidationError, validates_schema
from exception import BadParameterException
from modules.transaction.entity import Transaction
from modules.user.entity import User


class BalanceTransfer(Schema):
    amount = fields.Decimal(required=True)
    to_username = fields.String(required=True)

    @validates('amount')
    def amount_valid(self, value):
        if value <= 0:
            raise ValidationError("Invalid transfer amount")
        elif value > 10000000:
            raise ValidationError("Invalid transfer amount")

    @validates('to_username')
    def username_valid(self, value):
        user = User().find_by_username(value)
        if user is False:
            raise ValidationError("Destination user not found")

    @validates_schema
    def user_has_balance(self, data, **kwargs):
        user = User().find_by_username(data['to_username'])

        errors = {}
        if float(user.balance) <= float(data['amount']):
            errors["amount"] = ["Insufficient balance"]

        if errors:
            raise ValidationError(errors)

    def load_request(self, user, form):
        params = self.dump(form)

        errors = self.validate(params)
        if errors:
            raise BadParameterException(payload=errors)

        destination_user = User().find_by_username(params['to_username'])
        transaction = Transaction(type=Transaction.TYPE_TRANSFER_OUT, amount=float(params['amount']), actor=user, recipient=destination_user, status=Transaction.STATUS_SETTLED)

        return transaction
