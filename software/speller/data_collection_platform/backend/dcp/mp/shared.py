"""This file holds the shared variables between processes."""

from multiprocessing import Queue, Value, Manager

# creating a manager that will allow processes to be communicated to from the flask app
# the manager will control when processes can pull from the bci device
manager = Manager()
# {process_id: {
#   character : str, 
#   phase: float, 
#   frequency: float, 
#   q: Queue, 
#   config_id: int,
#   bci_config: str,
# , state: str (Could be either start, ready, collect, stop)
#   }
# }
bci_processes_states = manager.dict()
