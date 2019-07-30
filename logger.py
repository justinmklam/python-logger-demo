"""Custom Logger Module

Sets up a stdin/out stream handler and rotating file handler.
"""

import os
import sys
import datetime
import logging
from logging.handlers import RotatingFileHandler

from config import LOGGER_CONFIGS

def add_logger(name):
    """Add child logger to root logger

    Args:
        name (str): Name of child logger

    Returns:
        logger: Return a logger with the specified name
    """
    return logging.getLogger("%s.%s"%(LOGGER_CONFIGS["root_name"], name))

class Logger(object):
    def __init__(self, filename=None):
        """Initializes logger with stream and rotating file handlers.

        Args:
            filename (str): Log file name to use. If none is set, then default to root
                logger name

        Returns:
            logging.Logger: Logger handler
        """

        self.logger = logging.getLogger(LOGGER_CONFIGS["root_name"])
        self.logger.setLevel(LOGGER_CONFIGS["logging_level"])

        # This is a useful check if multiple classes will be importing this method.
        # It ensures that the logger only gets initialized once.
        if not self.logger.handlers:
            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] %(module)s.%(funcName)s: %(message)s"
            )
            sh = logging.StreamHandler()
            sh.setLevel(LOGGER_CONFIGS["logging_level"])
            sh.setFormatter(formatter)
            self.logger.addHandler(sh)

            if LOGGER_CONFIGS["log_to_file"]:
                self._initialize_file_logger(filename, formatter)

            # Logger handler for unhandled exception
            sys.excepthook = self._handle_exception

        self.logger.debug("Logger initialized.")

    def _initialize_file_logger(self, filename, formatter):
        if not os.path.exists(LOGGER_CONFIGS["directory"]):
            self.logger.debug("%s created." % LOGGER_CONFIGS["directory"])
            os.makedirs(LOGGER_CONFIGS["directory"])

        if filename is None:
            filename = LOGGER_CONFIGS["root_name"]

        fh = RotatingFileHandler(
            filename=os.path.join(LOGGER_CONFIGS["directory"], filename + ".log"),
            maxBytes=LOGGER_CONFIGS["max_size_of_single_log"],
            backupCount=LOGGER_CONFIGS["num_rotating_logs"],
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
