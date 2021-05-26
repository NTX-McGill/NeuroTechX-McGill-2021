from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

openbci_bp = Blueprint(name='openbci', import_name=__name__, url_prefix="/bci")

@openbci_bp.route("/stream", methods=["GET"])
def stream():
    # TODO @Thomas and @Abu
    return "streamed data", 200

