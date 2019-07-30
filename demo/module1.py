import logger

# Must match root logger name (in this case, 'my_logger')
log = logger.add_logger(__name__)

class MyModule1(object):
    """Example module to demonstrate from class methods.
    """

    def __init__(self):
        log.debug("Initializing class")

        self.myfunc()

    def myfunc(self):
        log.info("Doing stuff")

    def __del__(self):
        log.debug("Destroying class")
