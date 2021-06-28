from os import path, environ


class Config(object):
    """Configuration file"""

    SECRET_KEY = "my_secret_key"
    FLASK_ENV = 'development'
    FLASK_DEBUG = True
    BASE_DIR = path.dirname(path.abspath(__file__))
