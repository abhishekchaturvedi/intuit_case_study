from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, current_user
import logging
from flask.logging import default_handler
from celery import Celery
from celery.schedules import crontab

db = SQLAlchemy()
marshmallow = Marshmallow()
jwt = JWTManager()

from userlogin.blueprints.user import user
from userlogin.api.auth import AuthView
from userlogin.api.v1.users import UsersView
from userlogin.blueprints.user.models import User

formatter = logging.Formatter(
    '[%(asctime)s] %(module)s:%(funcName)s:%(lineno)d[%(levelname)s] %(message)s'
)

CELERY_TASKS = [userlogin.tasks]

def create_app():
    """
    This basic application will just bring up an HTTP serverself.
    Created based on flask documentation:
    https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application
    """

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py')

    app.logger.setLevel(app.config['LOG_LEVEL'])
    default_handler.setFormatter(formatter)

    app.logger.debug(app.config)
    app.register_blueprint(user)
    AuthView.register(app)
    UsersView.register(app)

    # Initialize extentions to our app.
    db.init_app(app)
    marshmallow.init_app(app)
    jwt.init_app(app)

    init_jwt_callbacks(app)
    app.jinja_env.globals.update(current_user=current_user)

    return app


def init_jwt_callbacks(app):
    """
    Setup behavior for JWT  based authentication. We can protect various API
    endpoints using the JWT authentication. However, for that to work, we need
    to ensure that flask-jwt has these callbacks setup. Each has different
    objective.

    user_loader_callback -- is called into whenever an endpoint is being
    accessed to setup the access token which was granted to the user when
    user successfully logged in.
    """

    @jwt.user_loader_callback_loader
    def user_loader_callback(identity):
        app.logger.debug("Loading user {0}".format(identity))
        return User.find_user(identity)


def create_celery_app():
    """
    Create a basic celery object and inform it to use settings from the config.
    We need to be able to provide tasks list to celery.
    see: https://flask.palletsprojects.com/en/0.12.x/patterns/celery/
    There are simpler ways to do this probably, but subclassing with Celery's
    base Task class gives the flask application context to the celery tasks.
    """

    app = create_app() # This is our flask app.
    # Just to try out -- Create simple periodic task
    # For this task to run, we need to make sure that celery also runs the
    # beat scheduler throuth it's command line.
    app.config['CELERYBEAT_SCHEDULE'] = {
                 'periodic-task-echo_every_1_min' : {
                     'task': 'echo_every_1_min',
                     'schedule' : crontab(minute="*")
                 }
             }
    celery = Celery(app.import_name,
                    broker=app.config['CELERY_BROKER_URL'],
                    backend=app.config['CELERY_RESULT_BACKEND'],
                    include=CELERY_TASKS)

    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
