import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'top-secret-key!'


class ProductionConfig(Config):
    DEBUG = False
    BACKUP_HOST = 'http://localhost:5080'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    BACKUP_HOST = 'http://localhost:5080'


class TestingConfig(Config):
    TESTING = True
    DEBUG = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
