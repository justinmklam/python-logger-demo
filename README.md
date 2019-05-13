# Python Logger Demo
Simple logging example in Python.

# Features

+ Prints log messages to console and file
+ Can specify the max size of each log, and how many logs to store
+ Each log message shows the file/module and function it came from
+ Logs unhandled exceptions

# Usage

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
