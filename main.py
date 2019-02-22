import os
import datetime
import logging
from logging.handlers import RotatingFileHandler

# Custom module to demonstrate how the logger interacts from another class
import module1

LOG_ROOT_NAME = 'my_logger'
LOG_FILE_DIRECTORY = "logs/"

LOG_TO_FILE = True
LOGGING_LEVEL = logging.DEBUG

MAX_SIZE_OF_SINGLE_LOG = 2e3 # in bytes (so 2KB in this case)
NUM_ROTATING_LOGS = 5

def setup_logger(root_name):
    """Initializes logger with stream and rotating file handlers.

    Args:
        root_name (str): Name of root logger to use

    Returns:
        logging.Logger: Logger handler
    """

    logger = logging.getLogger(root_name)
    logger.setLevel(LOGGING_LEVEL)

    # This is a useful check if multiple classes will be importing this method.
    # It ensures that the logger only gets initialized once.
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(module)s.%(funcName)s: %(message)s'
        )
        sh = logging.StreamHandler()
        sh.setLevel(LOGGING_LEVEL)
        sh.setFormatter(formatter)
        logger.addHandler(sh)

        if LOG_TO_FILE:
            if not os.path.exists(LOG_FILE_DIRECTORY):
                logger.debug('%s created.'%LOG_FILE_DIRECTORY)
                os.makedirs(LOG_FILE_DIRECTORY)

            # ie. my_logger_2019-02-22.log
            log_name = '%s_%s.log' % (root_name, str(datetime.datetime.today().strftime('%Y-%m-%d')))

            fh = RotatingFileHandler(
                filename=os.path.join(LOG_FILE_DIRECTORY, log_name),
                maxBytes=MAX_SIZE_OF_SINGLE_LOG,
                backupCount=NUM_ROTATING_LOGS
            )
            fh.setFormatter(formatter)
            logger.addHandler(fh)

        logger.debug('Logger initialized.')

    return logger

def demo_log_msgs(logger):
    """Logs messages at four logging levels.

    Args:
        logger (logging.Logger): Logger handler
    """

    logger.debug('This is a debug level message')
    logger.info('This is an info level message')
    logger.warning('This is a warning level message')
    logger.error('This is an error level message')

if __name__ == "__main__":
    logger = setup_logger(LOG_ROOT_NAME)

    demo_log_msgs(logger)

    logger.debug('Starting module 1')
    module1.MyModule1()

    logger.debug('Terminated.')
