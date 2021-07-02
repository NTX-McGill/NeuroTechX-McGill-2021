from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from celery import Celery

from dcp.cfg.config import app_configs

# FLASK EXTENSIONS
# global database object
db = SQLAlchemy()
migrate = Migrate()
celery = Celery(__name__, broker=app_configs.CELERY_BROKER_URL,
                backend=app_configs.CELERY_RESULT_BACKEND)


def create_app():
    app = Flask(__name__)

    app.config.from_object(app_configs)

    CORS(app)

    from . import api
    app.register_blueprint(api.bp)

    # initialize extensions
    db.init_app(app)
    celery.conf.update(app.config)

    # importing models so that Flask-Migrate can detect them
    from dcp.models.collection import CollectionInstance
    from dcp.models.configurations import OpenBCIConfig
    from dcp.models.data import CollectedData
    from dcp.models.video import Video
    migrate.init_app(app, db)


    return app
