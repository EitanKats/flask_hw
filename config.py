import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'top-secret-key!'


class ProductionConfig(Config):
    DEBUG = False
    NEIGHBOUR_ADDRESS = 'http://localhost:5080'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    NEIGHBOUR_ADDRESS = 'http://localhost:5080'


class TestingConfig(Config):
    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
