from flask import Blueprint, request
import dateutil.parser

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/anxious/start', methods=['POST'])
def anxiety_up():
    if not request.is_json:
        return {}, 400

    time = dateutil.parser.isoparse(request.json['time'])
    print(f"Anxious start at {time}")
    return {}, 200

@bp.route('/anxious/stop', methods=['POST'])
def anxiety_down():
    if not request.is_json:
        return {}, 400

    time = dateutil.parser.isoparse(request.json['time'])
    print(f"Anxious stop at {time}")
    return {}, 200
