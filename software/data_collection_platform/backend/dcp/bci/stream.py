import os
import logging
import signal
from pylsl import StreamInlet, resolve_stream

from dcp import db
from dcp.models.configurations import OpenBCIConfig
from dcp.mp.shared import (
    is_bci_ready,
    bci_config_id,
    is_video_playing, is_subject_anxious, q)

log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "logs",
                        "bci.log")

logging.basicConfig(filename=log_path,
                    level=logging.INFO,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s")

logger = logging.getLogger(__name__)


def stream_bci():
    """
    Method in charge of pulling data from the Open BCI device.
    This method will run in a separate process in parallel
    to the flask web application.
    Note that it is communicating with the flask application
    through 3 shared variables that are initialized in shared memory.
    """
    # ensure any remaining connections are flushed to avoid racing conditions
    db.engine.dispose()

    # first resolve an EEG stream on the lab network
    logger.info(
        "Attempting to connect to OpenBCI. Please make sure OpenBCI is open\
             with LSL enabled.")

    # Set up streaming over lsl from OpenBCI.
    # NOTE: this will block until a connection is established
    streams = resolve_stream('type', 'EEG')

    with is_bci_ready.get_lock():
        is_bci_ready.value = 1

    logger.info("Successfully connected to LSL stream.")

    # 0 picks up the first of three streams
    inlet = StreamInlet(streams[0])

    # get information about the stream
    bci_config = inlet.info().as_xml()
    logger.info(bci_config)

    # write configuration to database and store
    config = OpenBCIConfig(configuration=bci_config)

    # save current configuration to database
    db.session.add(config)
    db.session.commit()

    # an id is only assigned to an object after it is committed or flushed
    with bci_config_id.get_lock():
        bci_config_id.value = config.id

    # retrieve estimated time correction offset for the given stream - this is
    # the number that needs to be added to a timestamp that was remotely
    # generated via local_clock() to map it into the local clock domain for
    # this machine
    inlet.time_correction()

    running = True

    def on_exit(_sig, _stackframe):
        nonlocal running
        running = False

    signal.signal(signal.SIGINT, on_exit)
    signal.signal(signal.SIGTERM, on_exit)

    while running:

        # get a chunk of samples
        # ignoring the timestamps for now...
        samples, _timestamps = inlet.pull_chunk()

        if not samples:
            continue

        with is_video_playing.get_lock():
            if is_video_playing.value:

                with is_subject_anxious.get_lock():
                    q.put_nowait((samples, is_subject_anxious.value))

                logger.info(samples)
