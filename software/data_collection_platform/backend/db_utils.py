from dcp import db, create_app
import pandas as pd
from datetime import datetime

# although not used, important to import them in order to create the tables
from dcp.models.collection import CollectionInstance
from dcp.models.configurations import OpenBCIConfig
from dcp.models.data import CollectedData
from dcp.models.video import Video


def populate_videos(app):
    """Populate videos table in the database.
    """
    # read data team's google sheet using pandas
    SHEET_ID = "14f6uBw0FRok1X4-EnSj-A5HVW1AGEZDWvIRnwCLnOh8"
    URL = "https://docs.google.com/spreadsheets/d/{}/export?format=csv".format(
        SHEET_ID)

    with app.app_context():

        df = pd.read_csv(URL,
                         dtype={"start": str,
                                "end": str,
                                "link": str,
                                "stressful": int,
                                "keywords": str})

        # preprocess empty cells
        df.fillna("", inplace=True)

        # add the youtube_id column
        df["youtube_id"] = df.apply(
            lambda row: row.link.split("/")[-1], axis=1)

        # clear video table's content
        db.session.query(Video).delete()

        # add rows
        videos = [Video(
            youtube_id=row.youtube_id,
            start=datetime.strptime(row.start, "%M:%S") if row.start else None,
            end=datetime.strptime(row.end, "%M:%S") if row.end else None,
            is_stressful=bool(row.stressful),
            keywords=[keyword.strip() for keyword in row.keywords.split(";")],
            youtube_url=row.link,
        )
            for row in df.itertuples(index=False)
        ]
        db.session.add_all(videos)
        db.session.commit()


def create_tables(app):
    """We can either create all tables in our backend using this function
    or use Flask-Migrate.

    Instead of running this function, we could create the tables by running:
        - flask db upgrade
    """
    # use dcp app context to create all db tables
    db.create_all(app=app)


if __name__ == "__main__":
    app = create_app()
    populate_videos(app)
