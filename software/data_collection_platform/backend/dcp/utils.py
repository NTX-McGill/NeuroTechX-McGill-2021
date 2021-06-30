import csv
from . import db
from .models.video import Video

def null_if_empty(time_str):
    return None if len(time_str) == 0 else time_str
    
def save_videos():
    with open('./dcp/data/videos.csv', newline='') as videofile:
        reader = csv.reader(videofile, delimiter=',')
        next(reader) # Skip first line
        for row in reader:
            video = Video(youtube_id=row[0], start=null_if_empty(row[1]),
                          end=null_if_empty(row[2]), is_stressful=bool(row[3]), keywords=[word.strip() for word in row[4].split(";")])
            db.session.add(video)
    db.session.commit()
