from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class Video(Base):
    __tablename__ = "video"

    id = Column(String, primary_key=True)
    start = Column(String)
    end = Column(String)
    is_stressful = Column(Boolean)
    keywords = Column(String)
    video = relationship("collection_instance")
