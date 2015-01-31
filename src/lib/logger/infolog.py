""" The pySUMO informational log handler. Acts as an initializer for the python
logging framework and defines several convenience functions for working with
it.

This module contains:

- InfoLog: The informational log handler.

"""

import logging
import logging.handlers

from lib.logger import CONFIG_PATH
from os import makedirs
from os.path import dirname

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

    default_log_path = '/'.join([CONFIG_PATH, 'log'])
    default_socket_path = '/'.join([CONFIG_PATH, 'status'])

    def __init__(self, loglevel='WARNING', filename=default_log_path, socket_path=default_socket_path):
        """ Initializes the python logging framework.

        Kwargs:

        - loglevel: the loglevel above which entries are logged
        - filename: log location

        """
        self.filename = filename
        self.socket = socket_path
        try:
            makedirs(dirname(self.filename), exist_ok=True)
            makedirs(dirname(self.socket), exist_ok=True)
            self.f_handler = logging.handlers.RotatingFileHandler(self.filename, maxBytes=102400, backupCount=2)
            s_handler = logging.handlers.SocketHandler(self.socket, None)
        except PermissionError:
            makedirs(CONFIG_PATH, exist_ok=True)
            self.filename = self.default_log_path
            self.socket = self.default_socket_path
            self.f_handler = logging.handlers.RotatingFileHandler(self.filename, maxBytes=102400, backupCount=2)
            s_handler = logging.handlers.SocketHandler(self.socket, None)
        self.root_logger = logging.getLogger('')
        self.root_logger.setLevel(loglevel.upper())
        self.f_handler.setLevel(loglevel)
        s_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s: %(levelname)s:%(name)s:%(message)s')
        self.f_handler.setFormatter(formatter)
        s_handler.setFormatter(formatter)
        self.root_logger.addHandler(self.f_handler)
        self.root_logger.addHandler(s_handler)

    def set_loglevel(self, loglevel):
        """ Sets the loglevel above which to log messages. """
        self.f_handler.setLevel(loglevel)
