from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from celery import Celery

# FLASK EXTENSIONS
# global database object
db = SQLAlchemy()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)


def create_app():
    app = Flask(__name__)

    from dcp.cfg.config import app_configs
    app.config.from_object(app_configs)

    celery.conf.update(app.config)

    CORS(app)

    from . import api
    app.register_blueprint(api.bp)

    # initialize extensions
    db.init_app(app)

    return app
