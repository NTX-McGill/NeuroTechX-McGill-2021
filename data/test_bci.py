import os
import logging
from pylsl import StreamInlet, resolve_stream

test_file_path = "bci.log"

def stream_bci():
    # first resolve an EEG stream on the lab network
    print(
        "Attempting to connect to OpenBCI. Please make sure OpenBCI is open\
     with LSL enabled.")

    # Set up streaming over lsl from OpenBCI.
    # NOTE: this will block until a connection is established
    streams = resolve_stream('type', 'EEG')

    print("Successfully connected to LSL stream.")

    # 0 picks up the first of three streams
    inlet = StreamInlet(streams[0])

    # TODO: change "w" to "a" if you want to preserve previously collected points.
    with open(test_file_path, "w") as f:
        while True:

            # get a chunk of samples
            # ignoring the timestamps for now...
            samples, _timestamps = inlet.pull_chunk()

            if not samples:
                continue

            for sample in samples:
                sample_csv = ','.join([str(x) for x in sample])
                f.write(sample_csv)
                f.write('\n')

if __name__ == "__main__":
    stream_bci()
