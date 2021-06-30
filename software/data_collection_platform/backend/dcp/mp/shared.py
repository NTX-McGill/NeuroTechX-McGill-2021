""" This file holds the shared variables between processes """

from multiprocessing import Queue, Value
from ctypes import c_char_p

# queue is used as shared buffer allocated from shared memory 
# NOTE: using a queue for message passing between processes would be more efficient - the queue is unused for now but could be used for message passing
q = Queue(maxsize=0) # initialize queue size to infinite (bounded by memory)

# create shared variables that are process/thread safe to communicate between processes. These are ctypes object allocated from the shared memory
spacebar_status = Value("i", 0) # "i" follows typecodes used by the array module - see https://docs.python.org/3/library/array.html#module-array
video_playing_status = Value("i", 0)
bci_configuration = Value(c_char_p, None) # string holding the current OpenBCI configuration

# NOTE: anytime we want to write/read the shared variables, one must acquire and release the lock to avoid racing issues between processes/threads
