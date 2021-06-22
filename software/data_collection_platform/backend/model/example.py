import pyodbc
from sqlalchemy import create_engine
import urllib
import os

server = "tcp:mcgill-neurotech.database.windows.net,1433"
db = "McGill_NeuroTech"
usr = os.getenv("usr")
pwd = os.getenv("pwd")

params = urllib.parse.quote_plus(
    fr'DRIVER={{ODBC Driver 17 for SQL Server}};Server={server};Database={db};Uid={usr};Pwd={pwd};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
engine_azure = create_engine(conn_str, echo=True)

print('connection is ok')
print(engine_azure.table_names())
