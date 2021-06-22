from sqlalchemy import Column, Integer, String, DateTime, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


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
