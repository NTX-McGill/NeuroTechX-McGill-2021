from datetime import datetime
from functools import wraps
from re import L
from flask import Blueprint, request, current_app
import os

import dcp.mp.shared as shared
from dcp import db
from collections import deque
import time
from dcp.models.data import CollectedData
from dcp.models.collection import BCICollection
from dcp.signals.predict import predict_letter

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
                return {'error_message':
                        f'Missing fields: {", ".join(missing_fields)}'}, 400

            return f(*args, **kwargs)
        return decorated
    return decorator


@bp.route("/openbci/start", methods=['POST'])
def openbci_start():
    
    # TODO handle case where json is empty and return error
    if request.json is None:
        return {"error_message": "A json object with attributed 'collector_name' must be submitted"}, 400

    try:
        collector_name = request.json["collector_name"]
        current_app.logger.info(f"Current collect name is: {collector_name}.")
    except KeyError as e:
        return {'error_message': f'{e}. The \"collector_name\" attribute is missing from the json.'}, 400 

    # use a separate process to stream BCI data
    from dcp.bci.stream import stream_bci_api
    from multiprocessing import Process
    with current_app.app_context():
        # Although the subprocess gets initialized inside this scope, it will persist
        # bci_processes_states references this subprocess_dict
        shared.initialize_queue()
        subprocess_dict = shared.get_manager().dict({
            'character': None,
            'phase': None,
            'frequency': None,
            'collection_id': None,
            'bci_config': None,
            'state': None
        })
        
        # only pass this subprocess dict to ensure that locks are not too contentious
        p = Process(target=stream_bci_api, args=(subprocess_dict,shared.queue))
        # need to start process before referencing it to obtain the right process_id
        p.start()
        shared.get_bci_processes_states()[p.pid] = subprocess_dict

    BCI_CONNECT_TIMEOUT = 10
    start = time.time()
    while subprocess_dict['state'] != 'ready' or subprocess_dict['bci_config'] == None:
        current_app.logger.info("Trying to resolve BCI stream.")
        time.sleep(1)
        if (time.time() - start) > BCI_CONNECT_TIMEOUT:
            current_app.logger.info("BCI connection timeout, failed to resolve BCI stream.")
            p.kill()
            return {"error_message": "Server timeout"}, 408
    
    collection = BCICollection(bci_configuration=subprocess_dict['bci_config'],collector_name=collector_name)
    db.session.add(collection)
    db.session.commit()
    subprocess_dict['collection_id'] = collection.id
    # once the subprocess is ready, return from call
    return {"data": {"pid": p.pid}}, 201


@bp.route('/openbci/<int:process_id>/collect/start', methods=['POST'])
def openbci_process_collect_start(process_id: int):
    data = request.json

    print("Queue size:", shared.queue.qsize());

    if process_id not in shared.get_bci_processes_states():
        return {'error_message': f'There is no process with id {process_id}, make sure your process id is valid'}, 404
        
    subprocess_dict = shared.get_bci_processes_states()[process_id]

    if not data["predict"]:

        # We now know that the request contains all the key

        try:
            subprocess_dict['character'] = data['character']
            subprocess_dict['frequency'] = float(data['frequency'])
            subprocess_dict['phase'] = float(data['phase'])
        except KeyError as e:
            return {'error_message': f'Key {e} is missing from json.'}, 400
        except ValueError as e:
            return {'error_message': f'{e}. Make sure the data is the correct type: string for character, and float for phase and frequency.'}, 400

        subprocess_dict['state'] = 'collect'
        current_app.logger.info(
            f"BCI is collecting data for character \"{subprocess_dict['character']}\" with phase {subprocess_dict['phase']} and frequency {subprocess_dict['frequency']}.")

        return {'success_message': 'BCI is collecting.'}, 201

    else:

        subprocess_dict['state'] = 'collect'
        current_app.logger.info(
            f"BCI is collecting data for inference.")
        return {'success_message': 'BCI is collecting.'}, 201


@bp.route('/openbci/<int:process_id>/collect/stop', methods=['POST'])
def openbci_process_collect_stop(process_id: int):

    data = request.json

    subprocess_dict = shared.get_bci_processes_states()[process_id]
    subprocess_dict['state'] = 'ready'

    # if predict is false
    if not data["predict"]:

        if process_id not in shared.get_bci_processes_states():
            return {'error_message': 'There is no process with this id, make sure your process id is valid'}, 404

        current_app.logger.info(f"Stopped collecting for character {subprocess_dict['character']}.")
        current_app.logger.info(f"Writing collected data for character {subprocess_dict['character']} to the database.")

        # write to database
        if not write_stream_data(subprocess_dict):
            return {'error_message': "Did not write any data to the database, make sure to call /openbci/<int:process_id>/collect/start before this route."}, 400

        # clear the subprocess_dict
        subprocess_dict['character'] = None
        subprocess_dict['frequency'] = None
        subprocess_dict['phase'] = None

        return {'success_message': 'BCI has stopped collecting, and the queue has been written to the database'}, 201

    # run predict
    else:

        # TODO test the following if statement for error handling     
        if shared.queue.empty():
            return {"error_message": "Did not return prediction. Queue for BCI data is empty."}, 400

        # TODO test the following if statement for error handling
        if data["sentence"] is None:
            return {"error_message": "Sentence must be a string and cannot be a NoneType. Try using an empty string if sentence has length 0."}, 400
        
        print("Before clearing:", shared.queue.qsize())

        # call the matlab function with the EEG data in the shared queue
        next_character = predict_character(shared.queue)
        data["sentence"] += next_character

        while not shared.queue.empty():
            stream_data = shared.queue.get_nowait()

        print("After clearing:", shared.queue.qsize())

        # call the ML function for next word prediction or current word autocompletion
        #ml_predictions = dispatch(data["sentence"])

        # TODO check if 200 response code is the correct choice
        return {"sentence": data["sentence"], "next_character": next_character}, 200#, "predictions": ml_predictions["options"], "mode": ml_predictions["mode"]}, 200


def predict_character(shared_queue):
    """ Dummy function waiting for signal team """
    # pull out data from the shared queue
    bci_data = None
    while not shared.queue.empty():
        stream_data = shared.queue.get_nowait()
        print("Data sample:", np.asarray(stream_data).shape)
        bci_data = np.asarray(stream_data) if (bci_data is None) else np.concatenate((bci_data, np.asarray(stream_data)))

    print("Final shape:", bci_data.shape)
    
    return predict_letter(bci_data)

@bp.route("/openbci/<int:process_id>/stop", methods=['POST'])
def openbci_stop(process_id: int):

    if process_id not in shared.get_bci_processes_states():
        return {'error_message': 'There is no process with this id, make sure your process id is valid'}, 404
    
    subprocess_dict = shared.get_bci_processes_states()[process_id]
    if subprocess_dict['state'] == 'collect':
        subprocess_dict['state'] = 'stop'
        return {"error_message": f"Stopped bci process while it was collecting, data was not written for character {subprocess_dict['character']}."}, 400

    subprocess_dict['state'] = 'stop'
    if not shared.queue.empty():
        return {'error_message': f"Stopped bci process, however the queue for BCI data was not empty, data for character {subprocess_dict['character']} might be incomplete."}, 400
    
    try:
        collection = db.session.query(BCICollection).get(subprocess_dict['collection_id'])
        collection.collection_end_time = datetime.utcnow()
        db.session.commit()

        shared.get_bci_processes_states().pop(process_id)
    except Exception as e:
        return {'error_message': e.message}, 500

    return {'success_message': f"Successfully ended BCI subprocess with id {process_id}"}, 200


def write_stream_data(subprocess_dict):
    order = 1
    collected_data = []
    while not shared.queue.empty():
        stream_data = shared.queue.get_nowait()
        for row in stream_data:
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
                    collection_id=subprocess_dict['collection_id'],
                    character=subprocess_dict['character'],
                    frequency=subprocess_dict['frequency'],
                    phase=subprocess_dict['phase'],
                    order=order
                )
            )
            order += 1

    current_app.logger.info("Queue size after writing:", shared.queue.qsize())

    db.session.add_all(collected_data)
    db.session.commit()
    if len(collected_data) > 0:
        current_app.logger.info("Successfully wrote {} samples to the database.".format(len(collected_data)))
        return True
    return False
