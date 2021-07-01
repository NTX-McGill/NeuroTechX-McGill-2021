from dcp import create_app
from dcp.bci.stream import stream_bci
from dotenv import load_dotenv
from multiprocessing import Process

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
