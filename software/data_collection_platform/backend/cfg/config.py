import os 

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('DATABASE_URL', default='not_so_secret')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', default='sqlite:///test.db')

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True