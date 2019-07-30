# Custom logging module
import logger

# Custom module to demonstrate how the logger interacts from another class
import module1

log = logger.add_logger(__name__)

def demo_log_msgs():
    """Logs messages at four logging levels.

    Args:
        logger (logging.Logger): Logger handler
    """

    log.debug("This is a debug level message")
    log.info("This is an info level message")
    log.warning("This is a warning level message")
    log.error("This is an error level message")
    log.critical("This is a critical level message")


if __name__ == "__main__":
    demo_log_msgs()

    log.debug("Starting module 1")
    module1.MyModule1()

    raise RuntimeError("This unhandled error will be saved in the log")
