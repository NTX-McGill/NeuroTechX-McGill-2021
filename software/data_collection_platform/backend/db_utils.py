from dcp import create_app, db, current_app
from dotenv import load_dotenv
import pandas as pd

from dcp.models.collection import CollectionInstance
from dcp.models.configurations import OpenBCIConfig
from dcp.models.data import CollectedData
from dcp.models.video import Video


def populate_videos():
    """Populate videos table in the database.
    """
    with current_app.app_context():

        # data team google sheet
        URL = "https://docs.google.com/spreadsheets/d/14f6uBw0FRok1X4-EnSj-A5HVW1AGEZDWvIRnwCLnOh8/edit#gid=0"

        df = pd.read_csv(URL)
        df.to_sql(name=Video.__tablename__, con=db.engine, if_exists="append")


def create_tables():
    """We can either create all tables in our backend using this function or use Flask-Migrate.
    By running:
        - flask db upgrade
    """
    # use dcp app context to create all db tables
    db.create_all(app=create_app())


if __name__ == "__main__":
    # loading environment variables in .env
    load_dotenv()
