from pylsl import StreamInlet, resolve_stream
import logging

from dcp.mp.shared import *

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")

logger = logging.getLogger(__name__)


def stream_bci():
    """
    Method in charge of pulling data from the Open BCI device.
    This method will run in a separate process in parallel to the flask web application.
    Note that it is communicating with the flask application through 3 shared variables
    that are initialized in shared memory.
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

    # retrieve estimated time correction offset for the given stream - this is the number that needs to be added to a
    # time stamp that was remotely generated via local_clock() to map it into the local clock domain fo this machine
    inlet.time_correction()
    while True:

        # get a chunk of samples
        samples, _timestamps = inlet.pull_chunk()  # ignoring the timestamps for now...

        if not samples:
            continue

        with is_video_playing.get_lock():
            if is_video_playing.value:

                with is_subject_anxious.get_lock():
                    q.put_nowait((samples, bool(is_subject_anxious.value)))

                logger.info(samples)
