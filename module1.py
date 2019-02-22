import logging

import config

# Must match root logger name (in this case, 'my_logger')
logger = logging.getLogger("%s.%s"%(config.LOG_ROOT_NAME, __name__))

class MyModule1(object):
    """Example module to demonstrate from class methods.
    """

    def __init__(self):
        logger.debug("Initializing class")

        self.myfunc()

    def myfunc(self):
        logger.info("Doing stuff")

    def __del__(self):
        logger.debug("Destroying class")
