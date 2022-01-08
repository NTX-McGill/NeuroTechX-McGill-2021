"""
This file will allow the application to connect to the BCI process
and collect the brain signals being streamed
This code is based on
1. https://github.com/OpenBCI/OpenBCI_GUI/blob/master/Networking-Test-Kit/LSL/lslStreamTest.py
2. the previous years stream.py found at NeuroTechX-McGill-2021/software/data_collection_platform/backend/dcp/bci/stream.py
"""

from pylsl import StreamInlet, resolve_stream
import time 
import logging
import os

log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "logs",
                        "bci.log")

logging.basicConfig(filename=log_path,
                    level=logging.INFO,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s")

logger = logging.getLogger(__name__)
logger.info('test logger')

def stream_bci_api(bci_running): 
    # Some imports are only in this section, to allow other functions to be tested outside of the flask app
    # The relative import paths make this difficult to test in isolation
    # TODO: currently the collecting shared variable is in another branch, will have to test with other branch to see if this works
    # from dcp.mp.shared import collecting
    from dcp.mp.shared import q
    # TODO: this next import has to do with the DB, and reading the BCI config ID
    # will need to be done once the db is fully setup
    # from dcp.models.configurations import OpenBCIConfig

    # from multiprocessing import current_process
    logger.info('Attempting to initialize stream')

    inlet = connect_to_bci()

    logger.info('Succesfully connected to an inlet stream')
    logger.info(inlet.info().as_xml())

    # TODO: save current configuration to database once it is ready
    # db.session.add(config)
    # db.session.commit()

    # TAKEN FROM LAST YEAR:
    # retrieve estimated time correction offset for the given stream - this is
    # the number that needs to be added to a timestamp that was remotely
    # generated via local_clock() to map it into the local clock domain for
    # this machine
    inlet.time_correction()

    while bci_running[os.getpid()] == False:
        continue
        # this will ensure that there is no race condition, and that the parent process has been able to instantiate this variable

    # os.getpid()
    # running = True
    while bci_running[os.getpid()]:
        samples, _timestamps = inlet.pull_chunk()

        if not samples:
            continue
        # TODO: uncomment this section to check the collecting value
        # with collecting.get_lock():
        #     if collecting.value:
        q.put_nowait(samples)
    
        logger.info(samples)

    logger.info("no longer running")
    return 'success'


def connect_to_bci():
    # first resolve an EEG stream on the lab network
    # NOTE: this will block until a connection is established
    print("looking for an EEG stream...")
    streams = resolve_stream('type', 'EEG')

    print('connected to EEG streams')
    if len(streams) == 1:
        inlet = StreamInlet(streams[0])
        print('only 1 stream, we are good to proceed')
        # logger.info("Connected to stream.")

    # get information about the stream
    bci_config = inlet.info().as_xml()
    print(bci_config)
    return inlet

def testLSLSamplingRate(inlet, duration):
    start = time.time()
    totalNumSamples = 0
    validSamples = 0
    numChunks = 0
    print( "Testing Sampling Rates..." )

    while time.time() <= start + duration:
        # get chunks of samples
        chunk, timestamp = inlet.pull_chunk()
        if chunk:
            numChunks += 1
            # print( len(chunk) )
            totalNumSamples += len(chunk)
            # print(chunk);
            for sample in chunk:
                # print(sample)
                validSamples += 1

    print( "Number of Chunks and Samples == {} , {}".format(numChunks, totalNumSamples) )
    print( "Valid Samples and Duration == {} / {}".format(validSamples, duration) )
    print( "Avg Sampling Rate == {}".format(validSamples / duration) )

if __name__ == '__main__':
    duration = 5
    inlet = connect_to_bci()
    testLSLSamplingRate(inlet, duration)
    # while True:
    #     chunk, timestamp = inlet.pull_chunk()
    #     if chunk:
    #         print('got chunk')