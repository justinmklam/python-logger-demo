import os
import datetime
import logging
from logging.handlers import RotatingFileHandler

import config

# Custom module to demonstrate how the logger interacts from another class
import module1

def initialize_logger(root_name):
    """Initializes logger with stream and rotating file handlers.

    Args:
        root_name (str): Name of root logger to use

    Returns:
        logging.Logger: Logger handler
    """

    logger = logging.getLogger(root_name)
    logger.setLevel(config.LOGGING_LEVEL)

    # This is a useful check if multiple classes will be importing this method.
    # It ensures that the logger only gets initialized once.
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(module)s.%(funcName)s: %(message)s'
        )
        sh = logging.StreamHandler()
        sh.setLevel(config.LOGGING_LEVEL)
        sh.setFormatter(formatter)
        logger.addHandler(sh)

        if config.LOG_TO_FILE:
            if not os.path.exists(config.LOG_FILE_DIRECTORY):
                logger.debug('%s created.'%config.LOG_FILE_DIRECTORY)
                os.makedirs(config.LOG_FILE_DIRECTORY)

            fh = RotatingFileHandler(
                filename=os.path.join(config.LOG_FILE_DIRECTORY, root_name + '.log'),
                maxBytes=config.MAX_SIZE_OF_SINGLE_LOG,
                backupCount=config.NUM_ROTATING_LOGS
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
    logger = initialize_logger(config.LOG_ROOT_NAME)

    demo_log_msgs(logger)

    logger.debug('Starting module 1')
    module1.MyModule1()

    logger.debug('Terminated.')
