from sqlalchemy import Column, Integer, String, DateTime, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from sqlalchemy import create_engine, MetaData
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
    channel_1 = Column(Numeric)
    channel_2 = Column(Numeric)
    channel_3 = Column(Numeric)
    channel_4 = Column(Numeric)
    channel_5 = Column(Numeric)
    channel_6 = Column(Numeric)
    channel_7 = Column(Numeric)
    channel_8 = Column(Numeric)
    space_bar_status = Column(Boolean)
    collection_instance = Column(String, ForeignKey("collection_instance.id"))

    def __repr__(self):
        return str(self.__dict__)


@auto_str
class CollectionInstance(Base):
    __tablename__ = "collection_instance"

    id = Column(Integer, primary_key=True)
    stress_level = Column(Integer)
    video_id = Column(String, ForeignKey("video.id"))
    date = Column(DateTime, default=datetime.utcnow)
    video_id = Column(String, ForeignKey("video.id"))

    def __repr__(self):
        return str(self.__dict__)


@auto_str
class Video(Base):
    __tablename__ = "video"

    id = Column(String, primary_key=True)
    start = Column(String)
    end = Column(String)
    is_stressful = Column(Boolean)
    keywords = Column(String)

    def __repr__(self):
        return str(self.__dict__)
