"""This file holds the shared variables between processes."""

from multiprocessing import Queue, Value
import ctypes

# NOTE: anytime we want to write/read the shared variables, one must acquire and release the lock to avoid racing issues between processes/threads
# NOTE: we could use another queue for message passing between processes would be more efficient
# Queue's size is initialized to infinity (bounded by memory) and is used as shared buffer allocated from shared memory
q = Queue(maxsize=0)

# create shared variables that are process/thread safe to communicate between processes. These are ctypes object allocated from the shared memory
# "i" follows typecodes used by the array module - see https://docs.python.org/3/library/array.html#module-array
# TODO Stephen
character = Value("i", 0)
frequency = Value("i", 0)
phase = Value("i", 0)
collecting = Value(ctypes.c_bool, False)

# current BCI configuration id
bci_config_id = Value("i", 0)

# communicate whether the BCI device is ready (connected)
is_bci_ready = Value("i", 0)
