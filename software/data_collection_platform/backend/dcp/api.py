from functools import wraps
from flask import Blueprint, request
from dcp.mp.shared import *
from . import celery
import numpy as np
import pandas as pd


bp = Blueprint('api', __name__, url_prefix='/api')


def validate_json(*fields):
    """Decorator to validate JSON body.

    See https://flask.palletsprojects.com/en/2.0.x/patterns/viewdecorators/.
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not request.is_json:
                return {}, 400

            missing_fields = fields - request.json.keys()
            if len(missing_fields) > 0:
                return {'error': f'Missing fields: {", ".join(missing_fields)}'}, 400

            return f(*args, **kwargs)
        return decorated
    return decorator


@bp.route('/video/start', methods=['POST'])
@validate_json('time')
def video_start():
    with is_video_playing.get_lock():
        is_video_playing.value = 1

    return {}, 200


@bp.route('/video/stop', methods=['POST'])
@validate_json('time')
def video_stop():
    with is_video_playing.get_lock():
        is_video_playing.value = 0

    return {}, 200


@bp.route('/anxious/start', methods=['POST'])
@validate_json()
def anxious_start():
    with is_subject_anxious.get_lock():
        is_subject_anxious.value = 1

    return {}, 200


@bp.route('/anxious/stop', methods=['POST'])
@validate_json()
def anxious_stop():
    with is_subject_anxious.get_lock():
        is_subject_anxious.value = 0

    return {}, 200


@bp.route('/feedback', methods=['POST'])
@validate_json('url', 'stress_level')
def feedback():
    # TODO clear the buffer and store data to database this can be done using celery if we don't want this endpoint to hang ...
    # NOTE: frontend needs to send video_id and feedback

    url = request.json['url']
    feedback = request.json['stress_level']
    # clean queue
    df = pd.DataFrame()
    while not queue.empty():
        stream, anxious = queue.pop()
        # do some processing
        """
        we have
        [
            [1,2,3,4,5,6,7,8]
            [1,2,3,4,5,6,7,8]
            [1,2,3,4,5,6,7,8]
            [1,2,3,4,5,6,7,8]
            [1,2,3,4,5,6,7,8]
        ], 0
        
        
        we want into a df
        [
            [1,2,3,4,5,6,7,8], 1, 0
            [1,2,3,4,5,6,7,8], 2, 0
            [1,2,3,4,5,6,7,8], 3, 0
            [1,2,3,4,5,6,7,8], 4, 0
            [1,2,3,4,5,6,7,8], 5 ,0
        ]
        """
    write_to_db(df, feedback)
    print(f'Feedback for {url} is {feedback}')
    return {}, 200


@celery.task
def write_to_db(df, feedback):
    # convert df to python object then write to db
    """
    CollectionInstance = new CollectionInstance()

    CollectionInstance = feedback.stress leve
    CollectionInstance= feedback.video id
    CollectionInstance= collection time --> not needed.



    CollectedData = new CollectedData(
    CollectedData. collection_instance =  CollectionInstance
    set:
    - channels 1-8
    - order

    finally write to db
    """
    with bci_config_id.get_lock():
        configuration_id = bci_config_id.value
