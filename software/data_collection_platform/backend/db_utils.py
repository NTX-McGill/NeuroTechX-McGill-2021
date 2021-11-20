from dcp import db, create_app
import pandas as pd
from datetime import datetime, timedelta

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
        videos = Video.query.all()
        video_youtube_ids = [video.youtube_id for video in videos]

        def parse_timedelta(t: str):
            t = datetime.strptime(t, "%M:%S")
            return timedelta(minutes=t.minute, seconds=t.second)

        # add rows
        videos = [Video(
            youtube_id=row.youtube_id,
            start=parse_timedelta(row.start) if row.start != '' else None,
            end=parse_timedelta(row.end) if row.end != '' else None,
            is_stressful=bool(row.stressful),
            keywords=[keyword.strip() for keyword in row.keywords.split(";")],
            youtube_url=row.link,
        )
            for row in df.itertuples(index=False)
            if row.youtube_id not in video_youtube_ids
        ]
        db.session.add_all(videos)
        db.session.commit()

    print("Successfully wrote {} videos from {} to the video table.".format(
        len(videos), URL))


if __name__ == "__main__":
    app = create_app()
    populate_videos(app)
