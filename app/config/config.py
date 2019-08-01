from dotenv import load_dotenv
import os
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Config(object):
    """Config base class
        This is the default configuration class for app.
    """
    DEBUG = False
    TESTING = False
    ENV = 'development'
    SECRET_KEY = os.getenv('SECRET_KEY')


class DevelopmentConfig(Config):
    """Development Config.
        This extends the `Config` base class to store variables
        for development environments.
    """
    DEBUG = True
    FLASK_APP = 'APP-DEV'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    PORT = os.getenv('PORT') or 2000


class TestingConfig(Config):
    """Testing Config.
        This extends the `Config` base class to store variables
        for testing environments.
    """
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')


class StagingConfig(Config):
    """Staging Config.
       This extends the `Config` base class to store variables
       for staging environments.
    """
    pass


class ProductionConfig(Config):
    """Production Config
       This extends the `Config` base class to store variables
       for production environments
    """
    ENV = 'production'
