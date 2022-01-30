from dcp.models.utils import auto_str
from dcp import db


@auto_str
class BCICollection(db.Model):
    __tablename__ = "bci_collection"

    id = db.Column(db.Integer, primary_key=True)
    bci_configuration = db.Column(db.Text, nullable=False)
    collector_name = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return str(self.__dict__)
