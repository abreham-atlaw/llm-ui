import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

LOGGING = True
LOGGING_PID = True
LOGGING_CONSOLE = True
LOGGING_FILE_PATH = os.path.join(BASE_DIR, "out.log")

OPENAI_KEY = "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"

GAI_URL = "https://llmchat-server.vercel.app/api/"
