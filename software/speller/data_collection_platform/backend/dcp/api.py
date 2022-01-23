from functools import wraps
from flask import Blueprint, request, current_app
import os

import dcp.mp.shared as shared
from dcp import db
from collections import deque
import time
from dcp.models.data import CollectedData
from dcp.models.configurations import OpenBCIConfig


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

@bp.route("/openbci/start", methods=['POST'])
def openbci_start():
    # use a separate process to stream BCI data
    from dcp.bci.stream import stream_bci_api
    from multiprocessing import Process
    with current_app.app_context():
        # Although the subprocess gets initialized inside this scope, it will persist
        # bci_processes_states references this subprocess_dict
        subprocess_dict = {'params': shared.manager.dict({
                    'character': None,
                    'phase': None,
                    'frequency': None,
                    'config_id': None,
                    'bci_config': None,
                    'state': None
                }), 'q': shared.manager.Queue()}
        # only pass this subprocess dict to ensure that locks are not too contentious
        p = Process(target=stream_bci_api, args=(subprocess_dict['params'],))
        # need to start process before referencing it to obtain the right process_id
        p.start()
        shared.bci_processes_states[p.pid] = subprocess_dict['params']
    while subprocess_dict['params']['state'] != 'ready' or subprocess_dict['params']['bci_config'] == None:
        print('BCI NOT READY YET')
        time.sleep(1)
    config = OpenBCIConfig(configuration=subprocess_dict['params']['bci_config'])
    db.session.add(config)
    db.session.commit()
    subprocess_dict['params']['config_id'] = config.id
    # once the subprocess is ready, return from call
    return {"data": {"pid": p.pid}}, 201


@bp.route('/openbci/<int:process_id>/collect/start', methods=['POST'])
def openbci_process_collect_start(process_id:int):
    data = request.form
    expected_keys = ['character', 'phase' ,'frequency']
    for key in expected_keys:
        if key not in request.form.keys():
            return {'Invalid Request': 'Did not contain all attributes, make sure you send character, phase and frequency'}, 400
    # We now know that the request contains all the keys
    if process_id not in shared.bci_processes_states:
        return {'Invalid Request': 'There is no process with this id, make sure your process id is valid'}, 404
    subprocess_dict['params'] = shared.bci_processes_states[process_id]
    try:
        subprocess_dict['params']['character'] = data.get('character')
        subprocess_dict['params']['frequency'] = float(data.get('frequency'))
        subprocess_dict['params']['phase'] = float(data.get('phase'))
    except:
        return {'Invalid Request': 'Could not convert post form data. Make sure the data is the correct type. (string for character, and float for phase and frequency)'}, 400
    
    subprocess_dict['params']['state'] = 'collect'
    return {'Success': 'BCI is collecting'}, 201

@bp.route('/openbci/<int:process_id>/collect/stop', methods=['POST'])
def openbci_process_collect_stop(process_id:int):
    if process_id not in shared.bci_processes_states:
        return {'Invalid Request': 'There is no process with this id, make sure your process id is valid'}, 404
    subprocess_dict['params'] = shared.bci_processes_states[process_id]
    subprocess_dict['params']['state'] = 'ready'

    # write to database 
    if not write_stream_data(subprocess_dict['params']):
        return {'result': "Did not write any new information to database, stopping collection"}, 202
    # clear the subprocess_dict
    subprocess_dict['params']['character'] = None
    subprocess_dict['params']['frequency'] = None
    subprocess_dict['params']['phase'] = None
    subprocess_dict['q'] = shared.manager.Queue()

    return {'Success': 'BCI has stopped collecting, and the queue has been writen to the db'}, 201

@bp.route("/openbci/<int:process_id>/stop", methods=['POST'])
def openbci_stop(process_id: int):
    if process_id not in shared.bci_processes_states:
        return {'Invalid Request': 'There is no process with this id, make sure your process id is valid'}, 404
    subprocess_dict['params'] = shared.bci_processes_states[process_id]
    if subprocess_dict['params']['state'] == 'collect':
        subprocess_dict['params']['state'] = 'stop'
        return {"error": f"stopped bci process while it was collecting, data was not written for character {subprocess_dict['character']}"}, 400
    
    subprocess_dict['params']['state'] = 'stop'
    if subprocess_dict['q']:
        return {'warning': f"stopped bci process, however the queue for bci data was not empty, data for character {subprocess_dict['character']} might be incomplete"}, 400
    shared.bci_processes_states.pop(process_id, None)
    return {'success': f"ended subprocess with id {process_id}"}, 200

def write_stream_data(subprocess_dict):
    # ensure any remaining connections are flushed to avoid racing conditions
    db.engine.dispose()
    order = 1
    queue = subprocess_dict['q']
    collected_data = []
    while queue:
        stream_data = queue.popleft()
        for row in stream_data:
            if len(row) < 8:
                raise Exception("BCI Data is not the right format")
            collected_data.append(
                CollectedData(
                    channel_1=float(row[0]),
                    channel_2=float(row[1]),
                    channel_3=float(row[2]),
                    channel_4=float(row[3]),
                    channel_5=float(row[4]),
                    channel_6=float(row[5]),
                    channel_7=float(row[6]),
                    channel_8=float(row[7]),
                    config_id=subprocess_dict['params']['config_id'],
                    character=subprocess_dict['params']['character'],
                    frequency=subprocess_dict['params']['frequency'],
                    phase=subprocess_dict['params']['phase'],
                    order=order
                )
            )
            order += 1

    # logger.info(f"Collected data: {collected_data}")

    db.session.add_all(collected_data)
    db.session.commit()
    if len(collected_data) > 0:
        print("Successfully wrote {} samples.".format(len(collected_data)))
        return True
    return False
