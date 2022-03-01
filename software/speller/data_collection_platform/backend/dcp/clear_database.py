from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask import Blueprint

from dcp import db
from dcp.models.data import CollectedData
from dcp.models.collection import BCICollection


usersbp = Blueprint('users', __name__)


@usersbp.cli.command('clear')
def cleardb():
    db.session.query(CollectedData).delete()
    db.session.query(BCICollection).delete()
    db.session.commit()
    print("Deleted data")
