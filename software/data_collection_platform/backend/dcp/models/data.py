from dcp.models.utils import auto_str
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
    is_subject_anxious = db.Column(db.Boolean, nullable=False)
    collection_instance_id = db.Column(
        db.Integer, db.ForeignKey("collection_instance.id"), nullable=False)
    order = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return str(self.__dict__)
