from dcp.models.utils import auto_str
from dcp.models.collection import CollectionInstance
from dcp import db


@auto_str
class CollectedData(db.Model):

    __tablename__ = "collected_data"

    id = db.Column(db.Integer, primary_key=True)
    channel_1 = db.Column(db.Float, nullable=False)
    channel_2 = db.Column(db.Float, nullable=False)
    channel_3 = db.Column(db.Float, nullable=False)
    channel_4 = db.Column(db.Float, nullable=False)
    channel_5 = db.Column(db.Float, nullable=False)
    channel_6 = db.Column(db.Float, nullable=False)
    channel_7 = db.Column(db.Float, nullable=False)
    channel_8 = db.Column(db.Float, nullable=False)
    collection_instance_id = db.Column(
        db.Integer, db.ForeignKey(CollectionInstance.id), nullable=False)
    character = db.Column(db.String, nullable=False)
    frequency = db.Column(db.Float, nullable=False)
    phase = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return str(self.__dict__)
