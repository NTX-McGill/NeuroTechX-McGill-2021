"""This file holds the shared variables between processes."""

from multiprocessing import Queue, Manager

# creating a manager that will allow processes to be communicated to from the flask app
# the manager will control when processes can pull from the bci device
manager = None
bci_processes_states = None
queue = None

def get_manager():
    global manager
    if manager is None:
        manager = Manager()
    return manager

def initialize_queue():
    global queue
    queue = get_manager().Queue(maxsize=0)


def get_bci_processes_states():
    global bci_processes_states
    if bci_processes_states is None:
        bci_processes_states = get_manager().dict()
    return bci_processes_states

