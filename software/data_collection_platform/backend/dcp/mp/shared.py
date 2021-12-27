"""This file holds the shared variables between processes."""

from multiprocessing import Queue, Value

# NOTE: we could use another queue for message passing between processes would be more efficient
# Queue's size is initialized to infinity (bounded by memory) and is used as shared buffer allocated from shared memory
q = Queue(maxsize=0)

# create shared variables that are process/thread safe to communicate between processes. These are ctypes object allocated from the shared memory
# "i" follows typecodes used by the array module - see https://docs.python.org/3/library/array.html#module-array
is_subject_anxious = Value("i", 0)
is_video_playing = Value("i", 0)

current_character = Value("u", '\u0000')

# current configuration id
bci_config_id = Value("i", 0)

# whether the BCI is ready
is_bci_ready = Value("i", 0)

# NOTE: anytime we want to write/read the shared variables, one must acquire and release the lock to avoid racing issues between processes/threads
