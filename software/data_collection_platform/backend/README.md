# Data Collection Platform Backend

## Setup environment
1. Create environment using virtualvenv (Python 3.8):
    - For linux: `python -m venv dcp-env`
    - For Windows: `py -3 -m venv dcp-env`
2. Activate virtual environment: 
    - For Linux: `source dcp-env/bin/activate`
    - For Windows: `dcp-env\Scripts\activate.bat`
3. Install dependencies in newly created virtual environment: `pip install -r requirements.txt`

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


## Connect to db
1. Export database connection url as `DATABASE_URL`.
