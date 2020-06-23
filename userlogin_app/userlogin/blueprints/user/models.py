from werkzeug.security import generate_password_hash, check_password_hash
from userlogin.app import db
from sqlalchemy import DateTime

from collections import OrderedDict
import pytz
import datetime


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


    # Some stats.
    created_on = db.Column(DateTime(timezone=True),
                           default=datetime.datetime.now(pytz.utc))
    updated_on = db.Column(DateTime(timezone=True),
                           default=datetime.datetime.now(pytz.utc),
                           onupdate=datetime.datetime.now(pytz.utc))
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

    def authenticated(self, password=None):
        """
        Check if the user is authenticated by comparing the stored (hash)

        :param password: user's password
        :return: True if authenticated
        """
        assert password is not None
        return check_password_hash(self.password, password)

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
