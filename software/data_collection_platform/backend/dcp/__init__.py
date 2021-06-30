from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import os

### FLASK EXTENSIONS ###
# global database object
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ["APP_SETTINGS"])

    CORS(app)

    from . import api
    app.register_blueprint(api.bp)

    # initialize extensions
    db.init_app(app)

    return app

