
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import urllib
import pyodbc

from models import CollectedData, CollectionInstance, Video, Base


# server = "tcp:mcgill-neurotech.database.windows.net,1433"
# db = "McGill_NeuroTech"
# usr = os.getenv("usr")
# pwd = os.getenv("pwd")
# params = urllib.parse.quote_plus(
#     fr'DRIVER={{ODBC Driver 17 for SQL Server}};Server={server};Database={db};Uid={usr};Pwd={pwd};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
# conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
# engine = create_engine(conn_str, echo=True)


engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.bind = engine
Base.metadata.create_all(engine)
print('connection is ok')
print(engine.table_names())
DBSession = sessionmaker(bind=engine)

session = DBSession()


vid = Video(id="https://www.youtube.com/", start="1:10",
            end="2:20", is_stressful=False)

session.add(vid)
session.commit()


vids = [
    Video(id="https://www.youtube.com/1", start="1:10",
          end="2:20", is_stressful=False),
    Video(id="https://www.youtube.com/2", start="1:10",
          end="2:20", is_stressful=False),
    Video(id="https://www.youtube.com/3", start="1:10",
          end="2:20", is_stressful=False)
]

session.add_all(vids)


in_db = session.query(Video).filter_by(id='https://www.youtube.com/1').first()

print(in_db)
