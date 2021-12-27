import os

from flask import Flask, request

# DB setup to be added later

def create_app():
    app = Flask(__name__)

    # Configuration for the app
    # app.config.from_object(<config file>)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return ' '
    
    @app.route('/char_pressed', methods=['POST', 'GET'])
    def char_pressed():
        if request.method == 'POST':
            user_char_pressed = request.form['char_pressed']

    return app