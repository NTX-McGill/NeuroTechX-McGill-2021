"""This file holds the shared variables between processes."""

from multiprocessing import Queue, Value, Manager

# creating a manager that will allow processes to be communicated to from the flask app
# the manager will control when processes can pull from the bci device
manager = Manager()
# {process_id: {character, phase, frequency, q, config_id, collecting}}
bci_processes_states = manager.dict()
