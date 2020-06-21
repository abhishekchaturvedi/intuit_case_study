# Whether to print debug info.
DEBUG = True
LOG_LEVEL = 'DEBUG'


SQLALCHEMY_DATABASE_URI = 'postgresql://userlogin:devpassword@postgres:5432/userlogin'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# User.
SEED_ADMIN_EMAIL = 'dev@local.host'
SEED_ADMIN_PASSWORD = 'devpassword'
