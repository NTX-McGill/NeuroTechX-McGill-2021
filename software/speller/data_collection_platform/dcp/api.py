from functools import wraps
from flask import Blueprint, request, current_app
import signal
import os

import dcp.mp.shared as shared
from dcp import db
from dcp.models.collection import CollectionInstance

import numpy as np

bp = Blueprint('api', __name__, url_prefix='/api')


def validate_json(*fields):
    """Decorator to validate JSON body.

    See https://flask.palletsprojects.com/en/2.0.x/patterns/viewdecorators/.
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not request.is_json or not request.json:
                return {}, 400

            missing_fields = fields - request.json.keys()
            if len(missing_fields) > 0:
                return {'error':
                        f'Missing fields: {", ".join(missing_fields)}'}, 400

            return f(*args, **kwargs)
        return decorated
    return decorator


@bp.route('/')
def index():
    # TODO return keyboard layout
    return ' '


@bp.route('/char_pressed', methods=['POST', 'GET'])
def char_pressed():
    if request.method == 'POST':
        user_char_pressed = request.form['char_pressed']


@bp.route("/openbci/start", methods=['POST'])
def openbci_start():
    # use a separate process to stream BCI data
    from dcp.bci.stream import stream_bci
    from multiprocessing import Process
    with current_app.app_context():
        p = Process(target=stream_bci)
        p.start()
    return {"data": {"pid": p.pid}}, 201


@bp.route('/openbci/<int:process_id>/ready', methods=['GET'])
def openbci_ready(process_id: int):
    # NOTE: `pid` is currently ignored, see TODO in openbci_stop.
    with shared.is_bci_ready.get_lock():
        return {"data": bool(shared.is_bci_ready.value)}, 200


@bp.route("/openbci/<int:process_id>/stop", methods=['POST'])
def openbci_stop(process_id: int):
    # TODO: Might terminate the wrong process (!!).
    # We need some kind of process manager, and call
    # mp.Process.terminate() and mp.Process.kill() directly.
    # This would also allow us to use mp.Process.is_alive().
    os.kill(process_id, signal.SIGTERM)
    return {}, 200
