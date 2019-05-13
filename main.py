import os
import sys
import datetime
import logging
from logging.handlers import RotatingFileHandler

import config

# Custom module to demonstrate how the logger interacts from another class
import module1

class Logger(object):
    def __init__(self, filename=None):
        """Initializes logger with stream and rotating file handlers.

        Args:
            filename (str): Log file name to use. If none is set, then default to root
                logger name

        Returns:
            logging.Logger: Logger handler
        """

        self.logger = logging.getLogger(config.LOG_ROOT_NAME)
        self.logger.setLevel(config.LOGGING_LEVEL)

        # This is a useful check if multiple classes will be importing this method.
        # It ensures that the logger only gets initialized once.
        if not self.logger.handlers:
            formatter = logging.Formatter(
                '%(asctime)s [%(levelname)s] %(module)s.%(funcName)s: %(message)s'
            )
            sh = logging.StreamHandler()
            sh.setLevel(config.LOGGING_LEVEL)
            sh.setFormatter(formatter)
            self.logger.addHandler(sh)

            if config.LOG_TO_FILE:
                self._initialize_file_logger(filename, formatter)

            # Logger handler for unhandled exception
            sys.excepthook = self._handle_exception

        self.logger.debug('Logger initialized.')

    def _initialize_file_logger(self, filename, formatter):
        if not os.path.exists(config.LOG_FILE_DIRECTORY):
            self.logger.debug('%s created.'%config.LOG_FILE_DIRECTORY)
            os.makedirs(config.LOG_FILE_DIRECTORY)

        if filename is None:
            filename = config.LOG_ROOT_NAME

        fh = RotatingFileHandler(
            filename=os.path.join(config.LOG_FILE_DIRECTORY, filename + '.log'),
            maxBytes=config.MAX_SIZE_OF_SINGLE_LOG,
            backupCount=config.NUM_ROTATING_LOGS
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

        self.logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

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


def demo_log_msgs(logger):
    """Logs messages at four logging levels.

    Args:
        logger (logging.Logger): Logger handler
    """

    logger.debug('This is a debug level message')
    logger.info('This is an info level message')
    logger.warning('This is a warning level message')
    logger.error('This is an error level message')
    logger.critical('This is a critical level message')

if __name__ == "__main__":
    logger = Logger()

    demo_log_msgs(logger)

    logger.debug('Starting module 1')
    module1.MyModule1()

    raise RuntimeError("Unhandled error")
