"""Config file that contains global variables for configuring the logger.
"""

import logging

LOG_ROOT_NAME = 'my_logger'
LOG_FILE_DIRECTORY = "logs/"

LOG_TO_FILE = True
LOGGING_LEVEL = logging.DEBUG

MAX_SIZE_OF_SINGLE_LOG = 2e3 # in bytes (so 2KB in this case)
NUM_ROTATING_LOGS = 5
