import os
from flask import Flask
from flask_cors import CORS 

from . import openbci

def create_app(test_config=None):
    """ 
    Initialize the application in this function following application factory pattern.
    Any configuration, registration, and other setup for the application needs will happen inside this function, then the application will be returned.
    """

    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    
    # loading application configuration
    app.config.from_object("config.DefaultConfig")

    # set environment variables according to app.config
    os.environ["FLASK_APP"] = os.path.dirname(__file__)
    os.environ["FLASK_ENV"] = app.config["ENV"]
    os.environ["FLASK_DEBUG"] = str(app.config["DEBUG"])

    # example of routes, but better use blueprints for more modularized code..
    @app.route('/')
    def hello_world():
        return "Hello yolo world", 200

    # register blueprints from the factory
    app.register_blueprint(openbci.openbci_bp)

    return app