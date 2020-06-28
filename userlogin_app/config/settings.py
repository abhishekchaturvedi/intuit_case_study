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

# Celery.
CELERY_BROKER_URL = 'redis://:devpassword@redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://:devpassword@redis:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_REDIS_MAX_CONNECTIONS = 2
