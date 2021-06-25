from flask import Flask
from flask_cors import CORS 

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.DefaultConfig")

    CORS(app)

    from . import api
    app.register_blueprint(api.bp)

    from models import db
    db.init_app(app)

    return app
