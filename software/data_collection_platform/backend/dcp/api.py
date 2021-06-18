from functools import wraps
from flask import Blueprint, request
import dateutil.parser
from mp.shared import *

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
                return {'error': f'Missing fields {", ".join(missing_fields)}'}, 400

            return f(*args, **kwargs)
        return decorated
    return decorator


@bp.route('/video/start', methods=['POST'])
@validate_json('time')
def video_start():
    if not request.is_json:
        return {}, 400

    # acquire lock to modify shared variable
    with video_playing_status.get_lock():
        # set the variable to 1 to indicate that the video started
        video_playing_status.value = 1
    
    return {}, 200

@bp.route('/video/stop', methods=['POST'])
@validate_json('time')
def video_stop():
    if not request.is_json:
        return {}, 400
    
    # acquire lock to modify shared variable
    with video_playing_status.get_lock():
        # set the variable to 0 to indicate that the video ended
        if video_playing_status.value:
            video_playing_status.value = 0
    
    return {}, 200

@bp.route('/feedback', methods=['POST'])
@validate_json('url', 'stress_level')
def feedback():
    # TODO clear the buffer and store data to database this can be done using celery if we don't want this endpoint to hang ...
    # NOTE: frontend needs to send video_id and feedback

    url = request.json['url']
    feedback = request.json['stress_level']
    print(f'Feedback for {url} is {feedback}')
    return {}, 200

@bp.route('/anxious/start', methods=['POST'])
def spacebar_down():
    if not request.is_json:
        return {}, 400

    # acquire lock to modify shared variable
    with spacebar_status.get_lock():
        # set the variable to 1 to indicate that the space bar is held
        spacebar_status.value = 1
    
    return {}, 200

@bp.route('/anxious/stop', methods=['POST'])
def spacebar_up():
    if not request.is_json:
        return {}, 400
    
    # acquire lock to modify shared variable
    with spacebar_status.get_lock():
        # set the variable to 0 to indicate that the space bar is released
        if spacebar_status.value:
            spacebar_status.value = 0
    
    return {}, 200
