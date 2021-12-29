from functools import wraps
from flask import Blueprint, request, current_app
import signal
import os

import dcp.mp.shared as shared
from dcp import db, celery
from dcp.models.collection import CollectionInstance
from dcp.tasks import store_stream_data, add

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


@bp.route('/collection/start', method=['POST'])
def collection_start():
    """
    Starts the collection of data as the frontend
    starts highlighting a character

    Takes a JSON attachment with the following shape:
    {
        "data": {
            "character":    <character>,
            "phase":        <float>,
            "frequency"     <float>:
        }
    }
    """

    # TODO ensure JSON data structure is compatible

    json_data = request.get_json()

    # TODO write function to validate datatype

    with shared.collecting.get_lock():
        shared.collecting.value = True

    with shared.character.get_lock():
        shared.character.value = json_data["data"]["character"]

    with shared.frequency.get_lock():
        shared.character.value = json_data["data"]["frequency"]

    with shared.phase.get_lock():
        shared.character.value = json_data["data"]["phase"]

    return 200


@bp.route('/collection/stop', methods=['POST'])
def collection_stop():
    """
    Stops the collection of data as the frontend
    stops highlighting a character

    Takes a JSON attachment with the following shape:
    {
        "data": {
            "character":    <character>,
            "phase":        <float>,
            "frequency"     <float>:
        }
    }
    """

    json_data = request.get_json()

    with shared.collecting.get_lock():
        shared.collecting.value = False 
    
    # TODO implement adding queue items to database
    """
    while not shared.q.empty():
        # TODO verify that number of outputs is correct
        stream_data, character, frequency, phase = shared.q.get_nowait() 

        # TODO verify that collection object is correct
        data = np.asarray(stream_data, dtype=np.float32)
        data_point = CollectionInstance(stream_data, character, frequency, phase)
        
        # TODO verify placement of session commit() method
        db.session.add(data_point)
        db.session.commit()
    """

    # TODO change 501 to 200 when content is added to the database
    return 501


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


# CELERY TEST ROUTES
@bp.route('/tasks/<string:task_id>/status', methods=['GET'])
def get_task_status(task_id: str):
    """Return the state of a job given a task_id.

    Args:
        task_id ([str]): Celery task id
    """
    return {"result": celery.AsyncResult(task_id).state}, 200


@bp.route('/tasks/<string:task_id>/result', methods=['GET'])
def get_task_result(task_id: str):
    """Return the result of a job given a task_id.

    Args:
        task_id ([str]): Celery task id

    Returns:
        response: dictionary containing the result and the response code.
    """
    return {"result": celery.AsyncResult(task_id).result}, 200


@bp.route('/test', methods=['GET'])
def test():
    """Test Celery task queue setup.
    """
    import random
    a = random.randrange(1000)
    b = random.randrange(1000)
    r = add.apply_async(kwargs={"x": a, "y": b})

    # wait for messages by adding this line we make the call synchronous and
    # keep listening to messages
    r.get(on_message=lambda x: current_app.logger.info(x), propagate=False)
    return r.id, 200
