from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# FLASK EXTENSIONS
# global database object
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    from dcp.cfg.config import app_configs
    app.config.from_object(app_configs)

    CORS(app)

    from . import api
    app.register_blueprint(api.bp)

    # initialize extensions
    db.init_app(app)

    return app
