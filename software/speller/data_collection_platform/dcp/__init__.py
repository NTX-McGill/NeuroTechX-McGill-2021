import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from celery import Celery

from dcp.utils.celery import init_celery

from dcp.cfg.config import app_configs

# FLASK EXTENSIONS
# global database object
db = SQLAlchemy()
migrate = Migrate(compare_type=True)
cors = CORS()


def create_app():
    app = Flask(__name__)

    app.config.from_object(app_configs)

    # create logs directory if not exists
    os.makedirs(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "logs"), exist_ok=True)

    with app.app_context():
        from dcp import api
        app.register_blueprint(api.bp)

        # importing models so that Flask-Migrate can detect them
        from dcp.models.collection import CollectionInstance
        from dcp.models.configurations import OpenBCIConfig
        from dcp.models.data import CollectedData

        # # initialize extensions
        cors.init_app(app)
        db.init_app(app)
        db.create_all()  # creates all db tables (NOTE: will not recreate tables that already exist)
        migrate.init_app(app, db)

    return app
