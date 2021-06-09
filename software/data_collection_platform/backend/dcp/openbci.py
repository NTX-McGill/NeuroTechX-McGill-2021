from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

bp = Blueprint('openbci', __name__, url_prefix="/bci")

@bp.route("/stream", methods=["GET"])
def stream():
    # TODO @Thomas and @Abu
    return "streamed data", 200

