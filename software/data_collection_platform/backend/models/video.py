from models import auto_str, db

from sqlalchemy.types import ARRAY

@auto_str
class Video(db.Model):
    __tablename__ = "video"

    id = db.Column(db.Integer, primary_key=True)
    youtube_id = db.Column(db.String(50), nullable=False)
    start = db.Column(db.Time, nullable=True)
    end = db.Column(db.Time, nullable=True)
    is_stressful = db.Column(db.Boolean, nullable=False)
    keywords = db.Column(ARRAY(db.String))

    def __repr__(self):
        return str(self.__dict__)
