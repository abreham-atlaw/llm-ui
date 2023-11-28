import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

LOGGING = True
LOGGING_PID = True
LOGGING_CONSOLE = True
LOGGING_FILE_PATH = os.path.join(BASE_DIR, "out.log")

OPENAI_KEY = "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"

GAI_URL = "https://llmchat-server.vercel.app/api/"
