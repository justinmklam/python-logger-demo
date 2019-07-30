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


def add_logger(name):
    """Add child logger to root logger

    Args:
        name (str): Name of child logger

    Returns:
        logger: Return a logger with the specified name
    """
    return logging.getLogger("%s.%s"%(ROOT_NAME, name))


class Logger(object):
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

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    @property
    def streamhandler(self):
        return self.logger.handlers[0]

    @property
    def filehandler(self):
        return self.logger.handlers[1]

####

# This is required here so the logger handlers are initialized whenever the module is
# imported. Otherwise the logger will need to be manually initialized by the user.
Logger()
