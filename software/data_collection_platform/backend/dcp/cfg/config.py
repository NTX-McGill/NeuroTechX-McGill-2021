import os 

class Config(object):
    ENV = "production"
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='not_so_secret')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', default='sqlite:///test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True

class TestingConfig(Config):
    TESTING = True