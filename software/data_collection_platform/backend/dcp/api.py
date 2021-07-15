from functools import wraps
from flask import Blueprint, request, current_app
import signal
import os

import dcp.mp.shared as shared
from dcp import db, celery
from dcp.models.collection import CollectionInstance
from dcp.models.video import Video
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


@bp.route("/openbci/start", methods=['POST'])
def openbci_start():
    # use a separate process to stream BCI data
    from dcp.bci.stream import stream_bci
    from multiprocessing import Process
    p = Process(target=stream_bci)
    p.start()
    return {"data": p.pid}, 201


@bp.route("/openbci/<int:process_id>/stop", methods=['POST'])
def openbci_stop(process_id: int):
    # TODO: Might kill the wrong process (!!).
    # We need some kind of process manager, and call
    # mp.Process.terminate() and mp.Process.kill() directly.
    # This would also allow us to use mp.Process.is_alive().
    os.kill(process_id, signal.SIGKILL)
    return {}, 200


@bp.route('/openbci/<int:process_id>/ready', methods=['GET'])
def openbci_ready(process_id: int):
    # NOTE: `pid` is currently ignored, see TODO in openbci_stop.
    with shared.is_bci_ready.get_lock():
        return {"data": bool(shared.is_bci_ready.value)}, 200


@bp.route('/video/start', methods=['PUT'])
def video_start():
    with shared.is_video_playing.get_lock():
        shared.is_video_playing.value = 1

    return {}, 200


@bp.route('/video/stop', methods=['PUT'])
def video_stop():
    with shared.is_video_playing.get_lock():
        shared.is_video_playing.value = 0

    return {}, 200


@bp.route('/anxious/start', methods=['PUT'])
def anxious_start():
    with shared.is_subject_anxious.get_lock():
        shared.is_subject_anxious.value = 1

    return {}, 200


@bp.route('/anxious/stop', methods=['PUT'])
def anxious_stop():
    with shared.is_subject_anxious.get_lock():
        shared.is_subject_anxious.value = 0

    return {}, 200


@bp.route('/feedback', methods=['POST'])
@validate_json('video_id', 'stress_level')
def feedback():
    """Clear the buffer containing OpenBCI data once the feedback form is received.
    Store this data to the database by creating celery tasks that \
        write to the database.
    """

    video_id = request.json['video_id']
    feedback = request.json['stress_level']

    if not Video.query.get(video_id):
        return {"error": "Video is not in the database"}, 404

    if feedback < 0 or feedback > 3:
        return {"error":
                "Stress level must be between 0 and 3 inclusively."}, 400

    # create the collection instance
    with shared.bci_config_id.get_lock():
        configuration_id = shared.bci_config_id.value

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
    while not shared.q.empty():
        stream_data, is_anxious = shared.q.get_nowait()

        data = np.asarray(stream_data, dtype=np.float32)

        # add is_suject_anxious column
        is_subject_anxious = np.full((data.shape[0], 1), is_anxious)
        collection_instance_id = np.full((data.shape[0], 1), collection.id)
        sample_order = np.arange(
            order, order + data.shape[0]).reshape(data.shape[0], 1)
        data = np.hstack(
            (data, is_subject_anxious, collection_instance_id, sample_order))

        # update new value for order
        order += data.shape[0]

        try:
            tasks_ids.append(store_stream_data.apply_async(
                kwargs={"data": data.tolist()}).id)
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
                "start": video.start.total_seconds() if video.start else None,
                "end": video.end.total_seconds() if video.end else None,
                "is_stressful": video.is_stressful,
                "keywords": video.keywords,
                "youtube_id": video.youtube_id,
                "youtube_url": video.youtube_url,
            } for video in Video.query.all()]}, 200


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
