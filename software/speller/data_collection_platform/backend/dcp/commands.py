from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask import Blueprint

from dcp import db
from dcp.models.data import CollectedData
from dcp.models.collection import BCICollection


# Custom flask commands blueprint
commands_bp = Blueprint('commands', __name__)


# ADD COMMANDS HERE

@commands_bp.cli.command('cleardb')
def cleardb():
    db.session.query(CollectedData).delete()
    db.session.query(BCICollection).delete()
    db.session.commit()
    print("Deleted data")
