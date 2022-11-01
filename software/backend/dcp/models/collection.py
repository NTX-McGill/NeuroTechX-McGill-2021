from datetime import datetime
from dcp.models.utils import auto_str
from dcp import db


@auto_str
class BCICollection(db.Model):
    __tablename__ = "bci_collection"

    id = db.Column(db.Integer, primary_key=True)
    bci_configuration = db.Column(db.Text, nullable=False)
    collector_name = db.Column(db.Text, nullable=False)
    collection_start_time = db.Column(db.DateTime(
        timezone=True), default=datetime.utcnow, nullable=True)
    collection_end_time = db.Column(db.DateTime(
            timezone=True), nullable=True)
    
    def __repr__(self):
        return str(self.__dict__)
