from flask import Flask
from flask_cors import CORS 

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.DefaultConfig")

    CORS(app)

    from . import openbci
    app.register_blueprint(openbci.bp)

    return app
