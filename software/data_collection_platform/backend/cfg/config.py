# DEFAULT CONFIGURATIONS
import os 

class DefaultConfig(object):
    ENV = "development"
    SECRET_KEY = 'dev'
    DEBUG = True
    TESTING = False
    DATABASE = os.path.join(os.path.dirname(__file__), "instance\\flaskr.sqlite")