"""Custom Logger Module

Sets up a stdin/out stream handler and rotating file handler.
"""

import os
import sys
import datetime
import logging
from logging.handlers import RotatingFileHandler


ROOT_NAME = "my_logger"
LOG_DIRECTORY = "logs"
LOG_TO_FILE = True
LOG_LEVEL = logging.DEBUG
MAX_SIZE_OF_SINGLE_LOG = 2e3
NUM_ROTATING_LOGS = 5

# Remap of levels for easy access from external modules
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

def add_logger(name):
    """Add child logger to root logger

    Args:
        name (str): Name of child logger

    Returns:
        logger: Return a logger with the specified name
    """
    return logging.getLogger("%s.%s"%(ROOT_NAME, name))


class Logger(logging.Logger):
    def __init__(self, filename=None):
        """Initializes logger with stream and rotating file handlers.

        Args:
            filename (str): Log file name to use. If none is set, then default to root
                logger name

        Returns:
            logging.Logger: Logger handler
        """

        self.logger = logging.getLogger(ROOT_NAME)
        self.logger.setLevel(LOG_LEVEL)

        # This is a useful check if multiple classes will be importing this method.
        # It ensures that the logger only gets initialized once.
        if not self.logger.handlers:
            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] %(module)s.%(funcName)s: %(message)s"
            )
            sh = logging.StreamHandler()
            sh.setLevel(LOG_LEVEL)
            sh.setFormatter(formatter)
            self.logger.addHandler(sh)

            if LOG_TO_FILE:
                self._initialize_file_logger(filename, formatter)

            # Logger handler for unhandled exception
            sys.excepthook = self._handle_exception

            self.logger.debug("Logger initialized.")

    def _initialize_file_logger(self, filename, formatter):
        if not os.path.exists(LOG_DIRECTORY):
            self.logger.debug("%s created." % LOG_DIRECTORY)
            os.makedirs(LOG_DIRECTORY)

        if filename is None:
            filename = ROOT_NAME

        fh = RotatingFileHandler(
            filename=os.path.join(LOG_DIRECTORY, filename + ".log"),
            maxBytes=MAX_SIZE_OF_SINGLE_LOG,
            backupCount=NUM_ROTATING_LOGS,
        )
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def _handle_exception(self, exc_type, exc_value, exc_traceback):
        """Handle uncaught exceptions in python.

        - Ignores KeyboardInterrupt so a console program can exit with CTRL+C
        - This one changes the unhandled exception to go to stdout rather than stderr, but
        you could add all sorts of handlers in this same style to the logger object.

        Source: https://stackoverflow.com/a/16993115
        """
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        self.logger.error(
            "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
        )

    @property
    def streamhandler(self):
        return self.logger.handlers[0]

    @property
    def filehandler(self):
        return self.logger.handlers[1]

def set_streamhandler_level(level):
    """Set logging level for stream handler.

    Args:
        level (int): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    Logger().streamhandler.setLevel(level)

def set_filehandler_level(level):
    """Set logging level for file handler.

    Args:
        level (int): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    Logger().filehandler.setLevel(level)

def set_level(level):
    """Set logging level for stream and file handlers.

    Args:
        level (int): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    set_streamhandler_level(level)
    set_filehandler_level(level)

####

# This is required here so the logger handlers are initialized whenever the module is
# imported. Otherwise the logger will need to be manually initialized by the user.
Logger()
