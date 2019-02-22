# Python Logger Demo
Simple logging example in Python.

# Features

+ Prints log messages to console and file
+ Can specify the max size of each log, and how many logs to store
+ Each log message shows the file/module and function it came from

# Usage

To run the demo, simply execute:

```bash
python main.py
```

Example output:

```
2019-02-22 10:07:40,112 [DEBUG] main.setup_logger: Logger initialized.
2019-02-22 10:07:40,112 [DEBUG] main.demo_log_msgs: This is a debug level message
2019-02-22 10:07:40,112 [INFO] main.demo_log_msgs: This is an info level message
2019-02-22 10:07:40,113 [WARNING] main.demo_log_msgs: This is a warning level message
2019-02-22 10:07:40,113 [ERROR] main.demo_log_msgs: This is an error level message
2019-02-22 10:07:40,113 [DEBUG] main.<module>: Starting module 1
2019-02-22 10:07:40,113 [DEBUG] module1.__init__: Initializing class
2019-02-22 10:07:40,113 [INFO] module1.myfunc: Doing stuff
2019-02-22 10:07:40,113 [DEBUG] module1.__del__: Destroying class
2019-02-22 10:07:40,113 [DEBUG] main.<module>: Terminated.
```
