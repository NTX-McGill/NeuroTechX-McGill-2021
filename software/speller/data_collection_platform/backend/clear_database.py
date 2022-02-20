import click

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from dcp import db
from dcp.models.data import CollectedData
from dcp.models.collection import BCICollection


app = Flask(__name__)

# Gets rid of all the rows in
db.session.query(CollectedData).delete()
