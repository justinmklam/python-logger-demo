# Python Logger Demo

Simple logging example in Python with a custom module for common convenience operations.

## Features

+ Prints log messages to console and file
+ Can specify the max size of each log, and how many logs to store
+ Each log message shows the file/module and function it came from
+ Logs unhandled exceptions

## Usage

Simply add `logger.py` to your project and import it:

```python
import logger

# Use the file's name as the logger name
log = logger.add_logger(__name__)

log.debug("Hello World")
```

To change the logging level on a module level:

```python
log.setLevel(logger.INFO)
```

To change the logging levels for the handlers:

```python
# Set only the stream handler
logger.set_streamhandler_level(logger.INFO)

# Set only the file handler
logger.set_filehandler_level(logger.DEBUG)

# Set both handlers
logger.set_level(logger.WARNING)
```

Optional: Configure the global variables in `logger.py`:

| Variable | Type | Description |
|---|---|---|
| ROOT_NAME | str | Root logger name |
| LOG_DIRECTORY |  str | Directory to store logs (can be absolute or relative) |
| LOG_TO_FILE | bool | Whether to log to file or only to stdout |
| LOG_LEVEL | int | Logging level (DEBUG, INFO, WARNING, ERROR, or CRITICAL) |
| MAX_SIZE_OF_SINGLE_LOG_MB | float | Max size of single log for rotating file handler, in megabytes |
| NUM_ROTATING_LOGS | int | Number of rotating log files to keep before overwriting |


## Demo

To run the demo, simply execute:

```bash
python main.py
```

Example output:

```
2019-05-13 09:42:24,799 [INFO] main.info: This is an info level message
2019-05-13 09:42:24,800 [WARNING] main.warning: This is a warning level message
2019-05-13 09:42:24,800 [ERROR] main.error: This is an error level message
2019-05-13 09:42:24,800 [CRITICAL] main.critical: This is a critical level message
2019-05-13 09:42:24,800 [DEBUG] main.debug: Starting module 1
2019-05-13 09:42:24,800 [DEBUG] module1.__init__: Initializing class
2019-05-13 09:42:24,800 [INFO] module1.myfunc: Doing stuff
2019-05-13 09:42:24,800 [DEBUG] module1.__del__: Destroying class
2019-05-13 09:42:24,800 [ERROR] main._handle_exception: Uncaught exception
Traceback (most recent call last):
  File "main.py", line 114, in <module>
    raise RuntimeError("Unhandled error")
RuntimeError: Unhandled error
```
