# Custom logging module
import logger

# Custom module to demonstrate how the logger interacts from another class
import module1

logger = logger.add_logger(__name__)

def demo_log_msgs():
    """Logs messages at four logging levels.

    Args:
        logger (logging.Logger): Logger handler
    """

    logger.debug("This is a debug level message")
    logger.info("This is an info level message")
    logger.warning("This is a warning level message")
    logger.error("This is an error level message")
    logger.critical("This is a critical level message")


if __name__ == "__main__":
    demo_log_msgs()

    logger.debug("Starting module 1")
    module1.MyModule1()

    raise RuntimeError("This unhandled error will be saved in the log")
