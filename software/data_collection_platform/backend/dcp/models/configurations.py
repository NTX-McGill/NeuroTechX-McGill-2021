from dcp.models.utils import auto_str
from dcp import db


@auto_str
class OpenBCIConfig(db.Model):
    __tablename__ = "bci_config"

    id = db.Column(db.Integer, primary_key=True)
    configuration = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return str(self.__dict__)
