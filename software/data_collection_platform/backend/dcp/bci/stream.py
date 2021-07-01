from pylsl import StreamInlet, resolve_stream
import logging

from dcp import db

from models.configurations import OpenBCIConfig

from dcp.mp.shared import bci_config_id, is_video_playing, is_subject_anxious, q

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
    logger.info(bci_config)

    # write configuration to database and store
    config = OpenBCIConfig(configuration=bci_config)
    with bci_config_id.get_lock():
        bci_config_id.value = config.id

    # save current configuration to database
    db.session.add(config)
    db.session.commit()

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
                    q.put_nowait((samples, is_subject_anxious.value))

                logger.info(samples)
