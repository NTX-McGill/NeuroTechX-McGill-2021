from dcp import create_app
from multiprocessing import Process, Queue, Value
from bci.stream import stream_bci
import logging


if __name__ == "__main__":
    # use a separate process to stream BCI data 
    p = Process(target=stream_bci)
    p.start()

    # create and run flask app using current process
    app = create_app()
    app.run()

    # synchronize process
    p.join()
