from datetime import datetime

from dcp.models.utils import auto_str
from dcp import db

from sqlalchemy.orm import validates


@auto_str
class CollectionInstance(db.Model):
    __tablename__ = "collection_instance"

    id = db.Column(db.Integer, primary_key=True)
    stress_level = db.Column(db.Integer, nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"))
    collection_time = db.Column(db.DateTime(
        timezone=True), default=datetime.utcnow)
    config_id = db.Column(db.Integer, db.ForeignKey("bci_config.id"))

    @validates("stress_level")
    def validates_stress_level(self, key, stress_lv):
        assert 0 <= stress_lv <= 3
        return stress_lv

    def __repr__(self):
        return str(self.__dict__)
