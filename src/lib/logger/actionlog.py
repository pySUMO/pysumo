""" The pySUMO action log handler. This module handles undo and redo operations.

This module contains:

- ActionLog: The action log handler.
- LogIO: The action log io interface.

"""

from lib.logger import CONFIG_PATH

class ActionLog():
    """ The pySUMO action log. The SyntaxController queues a new log entry before every
    operation that makes changes to an Ontology, if the change is successful it OKs the
    entry in the log queue and the entry is written out. Log entries that are not OKed
    time out and are removed from the queue.

    Variables:

    - log_io: The io object for this log.
    - queue: A queue of actions that have not yet successfully completed.
    - actionlog: A list of actions that have completed successfully.
    - redolog: A list of actions that have been undone successfully.

    Methods:

    - queue_log: Create a log entry and append it to the log queue.
    - ok_log_item: Move log entry from log queue to actual log.
    - undo: Undoes the last action.
    - redo: Redoes the last undone action.

    """

    def __init__(self, path=None):
        """ Initializes the action log and instantiates variables. """
        self.log_io = LogIO(path)
        self.queue = {}
        self.actionlog = []
        self.redolog = []

    def _create_entry(self, data):
        """ Create a log entry from data.

        Args:

        - data: the data used to create the log entry

        Returns:

        - a log entry

        """

    def _append_entry(self, entry, log):
        """ Appends entry to log.

        Args:

        - entry: the entry to append
        - log: the log to append it to

        """

    def queue_log(self, data):
        """ Create a log entry and queue it for addition to self.actionlog.

        Args:

        - data: the data to be placed in the log

        Returns:

        - int. The log_queue_ok_num

        """

    def ok_log_item(self, log_queue_ok_num):
        """ Appends the item in self.queue with log_queue_ok_num to self.actionlog
        and calls self.log_io.append_write_queue on it.

        Args:

        - log_queue_ok_num: the number of the queue item to okay

        Raises:

        - KeyError

        """

    def undo(self):
        """ Undoes the last action and appends it to self.redolog. """

    def redo(self):
        """ Redoes the last undone action, appends it to self.undolog
        and removes it from self.redolog. """

class LogIO():
    """ The IO interface for the pySUMO action log. This class provides a storage
    backend for the Action Log. Entries in the write queue are written to disk
    after a timeout, or when the write queue reaches a maximum size.

    Variables:

    - path: The path to the logfile.
    - write_queue: The queue in which actions are stored before being written to disk.
    - timeout: The time period after which if no new packets have entered the queue, the queue is flushed.
    - max_size: The maximum number of actions in the write queue after which when another packet enters the queue, the queue is flushed.

    Methods:

    - write: Writes a full Action Log to path.
    - read: Instantiates an Action Log with the data in the stored log at path.
    - flush_write_queue: Appends all entries in the write queue to the log file.
    - append_write_queue: Appends an entry to the write queue.

    """

    default_path = ''

    def __init__(self, path):
        """ Initializes the IO interface for an action log. """
        self.path = LogIO.default_path if path is None else path
        self.write_queue = []
        self.timeout = 100
        self.max_size = 10

    def write(self, log):
        """ Writes log to self.path. """

    def read(self, log):
        """ Reads the log at self.path into log. """

    def flush_write_queue(self):
        """ Append all entries in self.write_queue to self.path. """

    def append_write_queue(self, entry):
        """ Append entry to self.write_queue. """
