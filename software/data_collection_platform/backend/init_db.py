from dcp import create_app, db
from dotenv import load_dotenv

"""Script used to initialize (create all tables) in the database."""

if __name__ == "__main__":
    # loading environment variables in .env
    load_dotenv()

    # use dcp app context to create all db tables
    db.create_all(app=create_app())
