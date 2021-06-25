from models import auto_str, db

@auto_str
class CollectedData(db.Model):

    __tablename__ = "collected_data"

    id = db.Column(db.Integer, primary_key=True)
    channel_1 = db.Column(db.Float)
    channel_2 = db.Column(db.Float)
    channel_3 = db.Column(db.Float)
    channel_4 = db.Column(db.Float)
    channel_5 = db.Column(db.Float)
    channel_6 = db.Column(db.Float)
    channel_7 = db.Column(db.Float)
    channel_8 = db.Column(db.Float)
    is_subject_anxious = db.Column(db.Boolean)
    collection_instance = db.Column(db.Integer, ForeignKey("collection_instance.id"))
    order = db.Column(db.Integer)

    def __repr__(self):
        return str(self.__dict__)