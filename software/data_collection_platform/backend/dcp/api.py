from functools import wraps
from flask import Blueprint, request

from dcp.mp.shared import is_subject_anxious, is_video_playing, q, bci_config_id
from dcp import celery, db

import numpy as np
import pandas as pd

from dcp.models.data import CollectedData
from dcp.models.collection import CollectionInstance

bp = Blueprint('api', __name__, url_prefix='/api')

# TODO add Flask logging


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
@validate_json('video_id', 'stress_level')
def feedback():
    """Clear the buffer containing OpenBCI data once the feedback form is received.
    Store this data to the database by creating celery tasks that write to the database. 
    """
    # TODO: frontend needs to send video_id and feedback

    video_id = request.json['video_id']
    feedback = request.json['stress_level']

    # create the collection instance
    with bci_config_id.get_lock():
        configuration_id = bci_config_id.value

    # create a collection instance
    collection = CollectionInstance(stress_level=feedback, video_id=video_id, config_id=configuration_id)

    # save current configuration to database
    db.session.add(collection)
    db.session.commit()

    # variable to keep track of the order of each samples
    order = 1

    # empty queue
    while not q.empty():

        stream_data, is_anxious = q.pop()

        # create a numpy array with
        data = np.asarray(stream_data, dtype=np.float32)

        # add is_suject_anxious column
        is_subject_anxious = np.full((data.shape[0], 1), is_anxious)
        collection_instance_id = np.full((data.shape[0], 1), collection.id)
        order = np.arange(order, order + data.shape[0]).reshape(data.shape[0], 1)
        data = np.hstack((data, is_subject_anxious, collection_instance_id))

        # update new value for order
        order += data.shape[0]

        store_stream_data(data)

    return {}, 200


@celery.task
def store_stream_data(data: np.ndarray):
    """Celery task responsible for storing a chunk of streamed data to the database.

    Args:
        data (numpy.ndarray): OpenBCI data to store to the database.
    """
    df = pd.DataFrame(data, columns=["channel_1", "channel_2", "channel_3", "channel_4", "channel_5", "channel_6",
                                     "channel_7", "channel_8", "is_subject_anxious", "collection_instance", "order"])
    df.to_sql(name=CollectedData.__tablename__, con=db.engine, if_exists="append")
