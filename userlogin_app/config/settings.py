# Whether to print debug info.
DEBUG = True
LOG_LEVEL = 'DEBUG'
TESTING = True
LOG_FORMATTER = '[%(asctime)s] %(levelname)s in %(module)s:%(funcName)s:%(lineno)d %(message)s'

SQLALCHEMY_DATABASE_URI = 'postgresql://userlogin:devpassword@postgres:5432/userlogin'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# User.
SEED_ADMIN_USERNAME = 'dev'
SEED_ADMIN_EMAIL = 'dev@local.host'
SEED_ADMIN_PASSWORD = 'devpassword'

SERVER_NAME = "0.0.0.0:8001"

SECRET_KEY = 'super-secret'
JWT_TOKEN_LOCATION = ['cookies', 'headers']
