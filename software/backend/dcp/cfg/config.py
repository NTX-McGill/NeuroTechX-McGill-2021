import os
from dotenv import load_dotenv

# loading environment variables in .env
load_dotenv()


class Config(object):
    ENV = "production"
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='not_so_secret')
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True, "pool_size": 5, "max_overflow": 10}
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    ENV = "development"

    # although ENV = `development` automatically sets DEBUG to True, it is
    # better to have it explicitly specified, as sometimes we want to
    # deactivate Flask reloading
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ['DEV_DATABASE_URL']


class TestingConfig(Config):
    TESTING = True


_configs = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': Config,
}

app_configs = _configs[os.environ["FLASK_ENV"]]
