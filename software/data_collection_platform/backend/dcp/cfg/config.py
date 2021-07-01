import os


class Config(object):
    ENV = "production"
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='not_so_secret')
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # cloudamqp Rabbit MQ
    CELERY_BROKER_URL = os.environ["MESSAGE_QUEUE_URL"]
    CELERY_RESULT_BACKEND = os.environ["MESSAGE_QUEUE_BACKEND"]


class DevelopmentConfig(Config):
    ENV = "development"

    # although ENV = `development` automatically sets DEBUG to True, it is
    # better to have it explicitly specified, as sometimes we want to deactivate Flask reloading
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ['DEV_DATABASE_URL']
    CELERY_BROKER_URL = os.environ["DEV_MESSAGE_QUEUE_URL"]


class TestingConfig(Config):
    TESTING = True


_configs = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': Config,
}

app_configs = _configs[os.environ["FLASK_ENV"]]
