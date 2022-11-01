"""
This file will allow the application to connect to the BCI process
and collect the brain signals being streamed
This code is based on
1. https://github.com/OpenBCI/OpenBCI_GUI/blob/master/Networking-Test-Kit/LSL/lslStreamTest.py
2. the previous years stream.py found at NeuroTechX-McGill-2021/software/data_collection_platform/backend/dcp/bci/stream.py
"""

from re import sub
from pylsl import StreamInlet, resolve_stream
import dcp.mp.shared as shared
import time 
import logging
import os

log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "logs",
                        "bci.log")

logging.basicConfig(filename=log_path,
                    level=logging.INFO,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s")

logger = logging.getLogger(__name__)

def stream_bci_api(subprocess_dict, queue): 

    logger.info('Attempting to initialize stream')

    inlet = connect_to_bci()

    logger.info('Succesfully connected to an inlet stream')
    bci_config = inlet.info().as_xml()
    logger.info(bci_config)
    subprocess_dict['bci_config'] = bci_config

    # TAKEN FROM LAST YEAR:
    # retrieve estimated time correction offset for the given stream - this is
    # the number that needs to be added to a timestamp that was remotely
    # generated via local_clock() to map it into the local clock domain for
    # this machine
    inlet.time_correction()
    subprocess_dict['state'] = 'ready'

    while subprocess_dict['state'] != 'stop':
        samples, _timestamps = inlet.pull_chunk()
        if not samples or subprocess_dict['state'] != 'collect':
            continue

        queue.put_nowait(samples)
        logger.info(samples)

    logger.info("Finished collecting BCI data.")
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