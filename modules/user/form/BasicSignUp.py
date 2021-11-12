from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length
from exception import BadParameterException

from modules.user.entity import User


class BasicSignUp(Schema):
    username = fields.String(required=True, validate=Length(max=180))

    @validates('username')
    def duplicate_username(self, value):
        rows = User().find(filters={"username": value})
        if len(rows) > 0:
            raise ValidationError("Username already exists")

    def load_request(self, form):
        params = self.dump(form)

        errors = self.validate(params)
        if errors:
            raise BadParameterException(payload=errors)

        return User().create_user(params['username'])
