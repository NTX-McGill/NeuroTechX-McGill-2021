from dcp import create_app, db
from dotenv import load_dotenv
from dcp.models.collection import CollectionInstance
from dcp.models.configurations import OpenBCIConfig
from dcp.models.data import CollectedData
from dcp.models.video import Video

""" Script used to initialize (create all tables) in the database. """

if __name__ == "__main__":
    # loading environment variables in .env
    load_dotenv() 

    # create and run flask app using current process
    db.create_all(app = create_app())