
from userlogin.app import marshmallow
from userlogin.blueprints.user.models import User

from marshmallow import validate, fields

class AuthSchema(marshmallow.Schema):
    username = fields.Str(required=True,
                          validate=validate.Length(min=3, max=255))
    password = fields.Str(required=True,
                          validate=validate.Length(min=8, max=128))


auth_schema = AuthSchema()
