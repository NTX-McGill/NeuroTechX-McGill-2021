from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, validates
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

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
class CollectedData(Base):

    __tablename__ = "collected_data"

    id = Column(Integer, primary_key=True)
    channel_1 = Column(Float)
    channel_2 = Column(Float)
    channel_3 = Column(Float)
    channel_4 = Column(Float)
    channel_5 = Column(Float)
    channel_6 = Column(Float)
    channel_7 = Column(Float)
    channel_8 = Column(Float)
    is_subject_anxious = Column(Boolean)
    collection_instance = Column(String, ForeignKey("collection_instance.id"))
    order = Column(Integer)

    def __repr__(self):
        return str(self.__dict__)


@auto_str
class CollectionInstance(Base):
    __tablename__ = "collection_instance"

    id = Column(Integer, primary_key=True)
    stress_level = Column(Integer)
    video_id = Column(String, ForeignKey("video.id"))
    date = Column(DateTime, default=datetime.utcnow, timezone=True)

    @validates("stress_level")
    def validates_stress_level(self, key, stress_lv):
        assert 1 <= stress_lv <= 3
        return stress_lv

    def __repr__(self):
        return str(self.__dict__)


@auto_str
class Video(Base):
    __tablename__ = "video"

    id = Column(String, primary_key=True)
    start = Column(Integer)
    end = Column(Integer)
    is_stressful = Column(Boolean)
    keywords = Column(String)

    def __repr__(self):
        return str(self.__dict__)
