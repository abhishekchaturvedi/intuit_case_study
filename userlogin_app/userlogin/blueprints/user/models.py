from werkzeug.security import generate_password_hash, check_password_hash
from userlogin.app import db
from sqlalchemy import DateTime
from flask import current_app
from itsdangerous import URLSafeTimedSerializer, TimedJSONWebSignatureSerializer

from collections import OrderedDict
import pytz
import datetime

def current_tztime():
    """
    return the current time in the current timezone
    """
    return datetime.datetime.now(pytz.utc)


class User(db.Model):
    """
    This is our user object.. or a row in the 'users' table
    """
    ROLES = OrderedDict([
        ('member', 'Member'),
        ('admin', 'Admin'),
    ])
    # Table to use.
    __tablename__ = "users"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    role = db.Column(db.Enum(*ROLES, name='role_types', native_enum=False),
                     index=True, nullable=False, server_default='member')

    # User info
    username = db.Column(db.String(32), unique=True, index=True)
    email = db.Column(db.String(255), unique=True, nullable=True,
                      server_default='')
    password = db.Column(db.String(128), nullable=False, server_default='')
    active = db.Column(db.Boolean, default=False, nullable=False,
                       server_default='0')

    # Some stats.
    created_on = db.Column(DateTime(timezone=True),
                           default=current_tztime)
    activated_on = db.Column(DateTime(timezone=True), default=None,
                             server_default=None)
    updated_on = db.Column(DateTime(timezone=True),
                           default=current_tztime,
                           onupdate=current_tztime)
    last_login = db.Column(DateTime(timezone=True),
                           default=None)
    last_signin_ip = db.Column(db.String(64))
    num_failed_attempts = db.Column(db.Integer, nullable=False, default=0)
    num_successful_attempts = db.Column(db.Integer, nullable=False, default=0)

    # .. additional fields can be added. Like last login from, etc.

    def __init__(self, **kwargs):
        """
        Pretty much just call the base class. But use our encryption.
        """
        super(User, self).__init__(**kwargs)
        self.password = User.encrypt_pass(kwargs.get('password', ''))

    @classmethod
    def encrypt_pass(cls, plaintext_pass):
        """
        encrypt password that's provided in plaintext_pass. If the password
        is empty or None, then return None.

        :param plaintext_pass: plain text password
        :return: encypted password.
        """
        if plaintext_pass:
            return generate_password_hash(plaintext_pass)
        return None

    @classmethod
    def find_user(cls, username):
        """
        Find the user based on their username or email.

        :param username: username/email to find
        :return: username object
        """
        return User.query.filter(
            (User.email == username) | (User.username == username)).first()

    @classmethod
    def initiate_activation(cls, user):
        if user.email is not None and user.email != '':
            activate_token = user.serialize_token()
            from userlogin.tasks import send_email
            send_email.delay(user.id, activate_token)
            return activate_token
        return None

    @classmethod
    def deserialize_token(cls, token):
        """
        deserializes a token which was previously generated for the user.

        :param token: the token which must have been generated using the
        serialize_token method on user's object.
        :return: user object if deserialization is successful, None otherwise.
        """
        private_key = current_app.config['SECRET_KEY']
        deserializer = TimedJSONWebSignatureSerializer(private_key)
        try:
            decoded = deserializer.loads(token)
            current_app.logger.debug("Decoded token: {0}".format(decoded))
            return User.find_user(decoded['user_email'])
        except Exception as e:
            current_app.logger.debug("Failed to decode token {0}".format(token))
            return None

    def serialize_token(self, expirein=600):
        """
        Create and sign a token to be used for one time workflows like
        registration/password reset etc.

        :param expirein: seconds before the token expires.
        :return: json object
        """
        private_key = current_app.config['SECRET_KEY']
        serializer = TimedJSONWebSignatureSerializer(private_key, expirein)
        return serializer.dumps({'user_email': self.email}).decode('utf-8')

    def authenticated(self, password=None):
        """
        Check if the user is authenticated by comparing the stored (hash)

        :param password: user's password
        :return: True if authenticated
        """
        assert password is not None
        return check_password_hash(self.password, password)

    def is_admin(self):
        """
        Check if the user has admin role

        :return: True if admin
        """
        return self.role == 'admin'

    def update_username(self, new_username):
        """
        Update user's Username

        :param new_username: New username
        :return: Updated username object
        """
        self.username = new_username
        self.save()
        return self

    def activate(self):
        """
        Mark the user active.
        """    
        self.active = True
        self.activated_on = current_tztime()
        self.save()

    def update_login(self, success=True, ipaddr=''):
        """
        Update user's Username

        :param success: Whether the login is successful or not
        :param ipaddr: IP address of the login.
        :return: Updated username object
        """
        if success:
            self.num_successful_attempts += 1
        else:
            self.num_failed_attempts += 1

        self.last_login = current_tztime()
        self.last_signin_ip = ipaddr
        self.save()
        return self

    def save(self):
        """
        Save a model instance.

        :return: Model instance
        """
        db.session.add(self)
        db.session.commit()

        return self

    def delete(self):
        """
        Delete a model instance.

        :return: db.session.commit()'s result
        """
        db.session.delete(self)
        return db.session.commit()

    def __str__(self):
        """
        Create a human readable version of a class instance.

        :return: self
        """
        obj_id = hex(id(self))
        columns = self.__table__.c.keys()

        values = ', '.join("%s=%r" % (n, getattr(self, n)) for n in columns)
        return '<%s %s(%s)>' % (obj_id, self.__class__.__name__, values)
