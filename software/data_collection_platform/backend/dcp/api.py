from functools import wraps
from flask import Blueprint, request, current_app

from dcp.mp.shared import (
    is_subject_anxious,
    is_video_playing,
    q,
    bci_config_id)
from dcp import db

import numpy as np

from dcp.models.collection import CollectionInstance
from dcp.models.video import Video

from dcp.tasks import store_stream_data

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
                return {'error':
                        f'Missing fields: {", ".join(missing_fields)}'}, 400

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
    Store this data to the database by creating celery tasks that \
        write to the database.
    """
    # TODO: frontend needs to send video_id and feedback

    video_id = request.json['video_id']
    feedback = request.json['stress_level']

    # create the collection instance
    with bci_config_id.get_lock():
        configuration_id = bci_config_id.value

    # create a collection instance
    collection = CollectionInstance(
        stress_level=feedback, video_id=video_id, config_id=configuration_id)

    # save current configuration to database
    db.session.add(collection)
    db.session.commit()

    # variable to keep track of the order of each samples
    order = 1

    # empty queue
    tasks_ids = []
    while not q.empty():
        stream_data, is_anxious = q.pop()

        data = np.asarray(stream_data, dtype=np.float32)

        # add is_suject_anxious column
        is_subject_anxious = np.full((data.shape[0], 1), is_anxious)
        collection_instance_id = np.full((data.shape[0], 1), collection.id)
        order = np.arange(
            order, order + data.shape[0]).reshape(data.shape[0], 1)
        data = np.hstack(
            (data, is_subject_anxious, collection_instance_id, order))

        # update new value for order
        order += data.shape[0]

        try:
            tasks_ids.append(store_stream_data.delay(data).id)
        except store_stream_data.OperationalError as exc:
            current_app.logger.exception("Sending task raised: %r", exc)

    # returning the task_id for each task so that frontend can check back
    # whether the task has completed or not later
    return {"tasks_ids": tasks_ids}, 200

@bp.route('/videos', methods=['GET'])
def get_videos():
    return {"data":
            [{
                "id": video.id,
                "start": video.start.strftime("%M:%S")
                if video.start else None,
                "end": video.end.strftime("%M:%S")
                if video.end else None,
                "is_stressful": video.is_stressful,
                "keywords": video.keywords,
                "youtube_id": video.youtube_id,
                "youtube_url": video.youtube_url,
            } for video in Video.query.all()]}, 200
