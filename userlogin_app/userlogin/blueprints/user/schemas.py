
from userlogin.app import marshmallow
from userlogin.blueprints.user.models import User

from marshmallow import validate, fields, ValidationError


def ensure_unique(data):
    user = User.find_user(data)

    # Not allowing exisitng user and 'all' as username.
    if user or data == 'all':
        raise ValidationError('{0} already exists'.format(data))

    return data

def ensure_exists(data):
    user = User.find_user(data)

    if not user:
        raise ValidationError('{0} does not exists'.format(data))

    return data


class AuthSchema(marshmallow.Schema):
    username = fields.Str(required=True,
                          validate=validate.Length(min=3, max=255))
    password = fields.Str(required=True,
                          validate=validate.Length(min=8, max=128))


class RegistrationSchema(marshmallow.Schema):
    email = fields.Email(required=True, validate=ensure_unique)
    username = fields.Str(required=True,
                          validate=[validate.Length(min=3, max=255),
                                    ensure_unique])
    password = fields.Str(required=True,
                          validate=validate.Length(min=8, max=128))


class UserSchema(marshmallow.Schema):
    class Meta:
        fields = ('created_on', 'username', 'email', 'active')


class UserSchemaDetailed(marshmallow.Schema):
    class Meta:
        fields = ('created_on', 'username', 'email',
                  'updated_on', 'last_login', 'last_signin_ip',
                  'num_failed_attempts', 'num_successful_attempts',
                  'active', 'activated_on')


class UserQuery(marshmallow.Schema):
    username = fields.Str(required=True,
                          validate=[validate.Length(min=3, max=255)])
    detailed = fields.Bool(required=False, missing=False)


class UserUpdateSchema(marshmallow.Schema):
    username = fields.Str(required=True,
                          validate=[validate.Length(min=3, max=255),
                                    ensure_exists])
    new_username = fields.Str(required=True,
                              validate=[validate.Length(min=3, max=255),
                                        ensure_unique])

class ActivationConfirmationSchema(marshmallow.Schema):
    token = fields.Str(required=True,)


auth_schema = AuthSchema()
registration_schema = RegistrationSchema()
users_schema = UserSchema(many=True)
user_schema = UserSchema()
user_query_schema = UserQuery()
user_update_schema = UserUpdateSchema()
user_schema_detailed = UserSchemaDetailed()
users_schema_detailed = UserSchemaDetailed(many=True)
confirm_schema = ActivationConfirmationSchema()
