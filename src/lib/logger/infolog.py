""" The pySUMO informational log handler. Acts as an initializer for the python
logging framework and defines several convenience functions for working with
it.

This module contains:

- InfoLog: The informational log handler.

"""

import logging

class InfoLog():
    """ The informational log handler for pySUMO. Initializes the python logging framework
    and contains several convenience functions. Instantiated only from the entry point.

    Variables:

    - default_log_path: The default path where the infolog will be stored.
    - filename: The location at which the infolog will be stored.
    - last_entry: The last entry in the infolog.

    Methods:

    - set_loglevel: Sets the loglevel above which to log messages.
    - get_log: Returns the complete log.
    - get_log_tail: Returns a subset of the most recent log messages.

    """

    default_log_path = ''

    def __init__(self, loglevel=logging.WARNING, filename=default_log_path):
        """ Initializes the python logging framework.

        Kwargs:

        - loglevel: the loglevel above which entries are logged
        - filename: log location

        """
        logging.basicConfig(filename=filename, level=loglevel)
        self.filename = filename
        self.last_entry = ''

    def set_loglevel(self, loglevel):
        """ Sets the loglevel above which to log messages. """

    def get_log(self):
        """ Returns the complete informational log. """

    def get_log_tail(self, num=10):
        """ Returns all new messages in the informational log, but at most num. """
