import time
from pylsl import StreamInlet, resolve_stream
import logging
import numpy as np

from dcp.mp.shared import *

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")

logger = logging.getLogger(__name__)

def stream_bci():
    """ 
    Method in charge of pulling data from the Open BCI device.
    This method will run in a separate process in parallel to the flask web application. 
    Note that it is communicating with the flask application through 3 shared variables that are initialized in shared memory.
    """
    # first resolve an EEG stream on the lab network
    logger.info("Attempting to connect to OpenBCI. Please make sure OpenBCI is open with LSL enabled.")

    # Set up streaming over lsl from OpenBCI. 
    streams = resolve_stream('type', 'EEG')
    
    # 0 picks up the first of three streams
    inlet = StreamInlet(streams[0])

    # get information about the stream 
    bci_config = inlet.info().as_xml()
    with bci_configuration.get_lock():
        bci_configuration.value = bci_config.encode("utf-8")
    logger.info(bci_config)
    
    # retrieve estimated time correction offset for the given stream - this is the number that needs to be added to a time stamp that was remotely generated via local_clock() to map it into the local clock domain fo this machine
    inlet.time_correction()
    while True:
        
        # get a chunk of samples
        samples, _timestamps = inlet.pull_chunk() # ignoring the timestamps for now...
        
        if not samples:
            continue

        with video_playing_status.get_lock():
            if video_playing_status.value: 

                with spacebar_status.get_lock():
                    spacebar_held = True if spacebar_status.value else False
                    q.put_nowait((samples, spacebar_held))

                logger.info(samples)
