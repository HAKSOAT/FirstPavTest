from flask import Flask
from .router import routes
from .utils.extensions import bcrypt, db


def create_app(config):
    """Instantiates Flask app.
        This creates a Flask application instance using
        application factory pattern with the config and
        returns an instance of the app with specified configurations

    :param config: Flask configuration from file
    :return: app
    """
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config)
    return app


def register_extensions(app):
    """Registers all app extensions.
        Extensions should be instantiated with the instance of the flask app

    :param app: Flask app instance
    :return: None
    """
    db.init_app(app)
    bcrypt.init_app(app)
    routes(app)
