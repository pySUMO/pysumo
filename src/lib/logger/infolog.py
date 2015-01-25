""" The pySUMO informational log handler. Acts as an initializer for the python
logging framework and defines several convenience functions for working with
it.

This module contains:

- InfoLog: The informational log handler.

"""

import logging
import logging.handlers

class InfoLog():
    """ The informational log handler for pySUMO. Initializes the python logging framework
    and contains several convenience functions. Instantiated only from the entry point.

    Variables:

    - default_log_path: The default path where the infolog will be stored.
    - default_socket_path: The default socket to which >=INFO logs will be sent.
    - filename: The location at which the infolog will be stored.
    - root_logger: The root logging object of which all other loggers are children.
    - f_handler: Sends messages to a file and rotates it when it becomes too large.
    - s_handler: Sends messages to a Unix socket.

    Methods:

    - set_loglevel: Sets the loglevel above which to log messages.

    """

    default_log_path = ''
    default_socket_path = ''

    def __init__(self, loglevel=logging.WARNING, filename=default_log_path, socket_path=default_socket_path):
        """ Initializes the python logging framework.

        Kwargs:

        - loglevel: the loglevel above which entries are logged
        - filename: log location

        """
        self.filename = filename
        self.root_logger = logging.getLogger('')
        self.root_logger.setLevel(loglevel)
        f_handler = logging.handlers.RotatingFileHandler(filename, maxBytes=102400, backupCount=2)
        f_handler.setLevel(loglevel)
        s_handler = logging.handlers.SocketHandler(socket_path, None)
        s_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s: %(levelname)s:%(name)s:%(message)s')
        f_handler.setFormatter(formatter)
        s_handler.setFormatter(formatter)
        self.root_logger.addHandler(f_handler)
        self.root_logger.addHandler(s_handler)

    def set_loglevel(self, loglevel):
        """ Sets the loglevel above which to log messages. """
        self.f_handler.setLevel(loglevel)
