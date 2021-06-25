from datetime import datetime

from models import auto_str, db

@auto_str
class CollectionInstance(db.Model):
    __tablename__ = "collection_instance"

    id = db.Column(db.Integer, primary_key=True)
    stress_level = db.Column(db.Integer) 
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"))
    date = db.Column(db.DateTime, default=datetime.utcnow, timezone=True)

    @validates("stress_level")
    def validates_stress_level(self, key, stress_lv):
        assert 0 <= stress_lv <= 3
        return stress_lv

    def __repr__(self):
        return str(self.__dict__)