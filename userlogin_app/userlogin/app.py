from flask import Flask
from userlogin.blueprints.user import user
from userlogin.api.auth import AuthView

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
    app.logger.debug("Set the log level to debug")
    app.register_blueprint(user)
    AuthView.register(app)

    @app.route('/')
    def index():
        """
        Render the welcome response.
        """
        return "Start of Intuit case study!"

    return app
