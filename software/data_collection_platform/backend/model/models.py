from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()

Base = declarative_base()


def auto_str(cls):
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )
    cls.__str__ = __str__
    return cls


@auto_str
class CollectedData(db.Model):

    __tablename__ = "collected_data"

    id = db.Column(db.Integer, primary_key=True)
    channel_1 = db.Column(db.Float)
    channel_2 = db.Column(db.Float)
    channel_3 = db.Column(db.Float)
    channel_4 = db.Column(db.Float)
    channel_5 = db.Column(db.Float)
    channel_6 = db.Column(db.Float)
    channel_7 = db.Column(db.Float)
    channel_8 = db.Column(db.Float)
    is_subject_anxious = db.Column(db.Boolean)
    collection_instance = db.Column(db.String, ForeignKey("collection_instance.id"))
    order = db.Column(db.Integer)

    def __repr__(self):
        return str(self.__dict__)


@auto_str
class CollectionInstance(db.Model):
    __tablename__ = "collection_instance"

    id = db.Column(db.Integer, primary_key=True)
    stress_level = db.Column(db.Integer)
    video_id = db.Column(db.String, db.ForeignKey("video.id"))
    date = db.Column(db.DateTime, default=datetime.utcnow, timezone=True)

    @validates("stress_level")
    def validates_stress_level(self, key, stress_lv):
        assert 1 <= stress_lv <= 3
        return stress_lv

    def __repr__(self):
        return str(self.__dict__)


@auto_str
class Video(db.Model):
    __tablename__ = "video"

    id = db.Column(db.String, primary_key=True)
    start = db.Column(db.Integer)
    end = db.Column(db.Integer)
    is_stressful = db.Column(db.Boolean)
    keywords = db.Column(db.String)

    def __repr__(self):
        return str(self.__dict__)
