import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

LOGGING = True
LOGGING_PID = True
LOGGING_CONSOLE = True
LOGGING_FILE_PATH = os.path.join(BASE_DIR, "out.log")
