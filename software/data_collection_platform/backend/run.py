from dcp import create_app
from multiprocessing import Process, Queue, Value
from bci.stream import stream_bci
import logging
from dotenv import load_dotenv

if __name__ == "__main__":
    # loading environment variables in .env
    load_dotenv() 
    
    # use a separate process to stream BCI data 
    p = Process(target=stream_bci)
    p.start()

    # create and run flask app using current process
    app = create_app()
    app.run()

    # synchronize process
    p.join()
