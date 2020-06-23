from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
import logging
from flask.logging import default_handler

db = SQLAlchemy()
marshmallow = Marshmallow()
jwt = JWTManager()

from userlogin.blueprints.user import user
from userlogin.api.auth import AuthView

formatter = logging.Formatter(
    '[%(asctime)s] %(module)s:%(funcName)s:%(lineno)d[%(levelname)s] %(message)s'
)

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

    # Initialize extentions to our app.
    db.init_app(app)
    marshmallow.init_app(app)
    jwt.init_app(app)

    return app
