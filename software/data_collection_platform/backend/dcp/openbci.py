from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

"""Example program to show how to read a multi-channel time series from LSL."""
import time
from pylsl import StreamInlet, resolve_stream
from time import sleep

bp = Blueprint('openbci', __name__, url_prefix="/bci")

@bp.route("/stream", methods=["GET"])
def stream():
# Taken from https://github.com/OpenBCI/OpenBCI_GUI/blob/master/Networking-Test-Kit/LSL/lslStreamTest.py
    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")
    streams = resolve_stream('type', 'EEG')

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])
    duration = 2

    sleep(1)
    start = time.time()
    totalNumSamples = 0
    validSamples = 0
    numChunks = 0
    stringToReturn = ""

    while time.time() <= start + duration:
        # get chunks of samples
        samples, timestamp = inlet.pull_chunk()
        if samples:
            numChunks += 1
            print( len(samples) )
            totalNumSamples += len(samples)
            # print(samples);
            for sample in samples:
                stringToReturn += str(sample)
                print(sample)
                validSamples += 1

    print( "Number of Chunks and Samples == {} , {}".format(numChunks, totalNumSamples) )
    print( "Valid Samples and Duration == {} / {}".format(validSamples, duration) )
    print( "Avg Sampling Rate == {}".format(validSamples / duration) )
    return stringToReturn, 200

