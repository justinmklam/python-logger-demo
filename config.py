"""Config file that contains global variables for configuring the logger.
"""

import logging

LOGGER_CONFIGS = {
    "root_name": "my_logger",
    "directory": "logs",
    "log_to_file": True,
    "logging_level": logging.DEBUG,
    "max_size_of_single_log": 2e3,  # in bytes (so 2KB in this case)
    "num_rotating_logs": 5,
}
