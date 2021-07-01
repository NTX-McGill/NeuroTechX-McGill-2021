from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# FLASK EXTENSIONS
# global database object
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    from dcp.cfg.config import app_configs
    app.config.from_object(app_configs)

    CORS(app)

    from . import api
    app.register_blueprint(api.bp)

    # initialize extensions
    db.init_app(app)

    # importing models so that Flask-Migrate can detect them
    from dcp.models.collection import CollectionInstance
    from dcp.models.configurations import OpenBCIConfig
    from dcp.models.data import CollectedData
    from dcp.models.video import Video
    migrate.init_app(app, db)

    return app
