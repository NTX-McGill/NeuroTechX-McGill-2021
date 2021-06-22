from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from video import Video

Base = declarative_base()


class CollectionInstance(Base):
    __tablename__ = "collection_instance"

    id = Column(Integer, primary_key=True)
    stress_level = Column(Integer)
    video_id = Column(String, ForeignKey("video.id"))
    date = Column(DateTime, default=datetime.utcnow)
    collected_data = relationship("collected_data")
