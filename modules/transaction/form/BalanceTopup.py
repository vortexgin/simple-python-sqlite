from marshmallow import Schema, fields, validates, ValidationError
from exception import BadParameterException
from modules.transaction.entity import Transaction


class BalanceTopup(Schema):
    amount = fields.Decimal(required=True)

    @validates('amount')
    def amount_valid(self, value):
        if value <= 0:
            raise ValidationError("Invalid topup amount")
        elif value > 10000000:
            raise ValidationError("Invalid topup amount")

    def load_request(self, user, form):
        params = self.dump(form)

        errors = self.validate(params)
        if errors:
            raise BadParameterException(payload=errors)

        transaction = Transaction(type=Transaction.TYPE_TOPUP_BALANCE, amount=float(params['amount']), actor=user, recipient=user, status=Transaction.STATUS_SETTLED)

        return transaction
