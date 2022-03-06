import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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
    logs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "logs")
    os.makedirs(logs_path, exist_ok=True)

    # configure logging
    import logging
    log_path = os.path.join(logs_path, "dcp.log")
    logging.basicConfig(filename=log_path, level=logging.DEBUG)

    with app.app_context():
        from dcp import api
        app.register_blueprint(api.bp)

        # importing models so that Flask-Migrate can detect them
        from dcp.models.collection import BCICollection
        from dcp.models.data import CollectedData

        # # initialize extensions
        cors.init_app(app)
        db.init_app(app)
        db.create_all()  # creates all db tables (NOTE: will not recreate tables that already exist)
        migrate.init_app(app, db)

        # Added blueprint for clearing the database
        from dcp.commands import commands_bp
        app.register_blueprint(commands_bp)

    return app
