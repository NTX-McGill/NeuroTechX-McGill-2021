# Data Collection Platform Backend

## Setup environment
1. Create environment using virtualvenv (Python 3.8):
    - For Linux: `python -m venv dcp-env`
    - For Windows: `py -3 -m venv dcp-env`
2. Activate virtual environment: 
    - For Linux: `source dcp-env/bin/activate`
    - For Windows: `dcp-env\Scripts\activate.bat`
3. Install dependencies in newly created virtual environment: `pip install -r requirements.txt`

Note that one can also use conda to create the environment: `conda create env dcp python=3.8`
Then install the dependencies as usual: `pip install -r requirements.txt`

## Running the application

```
$ python run.py
```

## Connecting to OpenBCI GUI with synthetic data
1. Download the OpenBCI GUI
   - https://openbci.com/downloads

2. Open the app, click "Synthetic (algorithmic)" --> "8 chan" --> START SESSION --> Start Data Stream.
3. Select "Networking" on one of the dropdowns, choose LSL protocol, select a data type (TimeSeries) then click "Start LSL Stream"
4. Run the application as shown above
5. Open a web browser and go to URLSHOWNINCONSOLEFORFLASKAPP/bci/stream


## Connecting to the database
The database credentials can be found on the software channel on Slack.
One can use the `psql` CLI to connect to the database: `psql --host=neurotech-db.postgres.database.azure.com --port=5432 --username=neurotech@neurotech-db --dbname=postgres`

Alternatively, see https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#a-minimal-application to interact with the database using python.

For example:
```
>>> from models.data import CollectedData
>>> CollectedData.query.all()
[<CollectedData>, ..., <CollectedData>]
```