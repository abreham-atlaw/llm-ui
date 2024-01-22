import os
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

LOGGING = True
LOGGING_PID = True
LOGGING_CONSOLE = False

OPENAI_KEY = "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"

LLM_TEMPERATURE = 0.01


GAI_URL = "https://llmchat-server.vercel.app/api/"

PROJECT_PATH = os.path.abspath("/home/abreham/Projects/TeamProjects/LLM-UI/temp/projects/orbit/web/orbit-website")
PROJECT_CONFIG_PATH = os.path.join(PROJECT_PATH, ".cop")
ANALYSIS_SAVE_PATH = os.path.join(PROJECT_CONFIG_PATH, "analysis.json")
ENVIRON_PATH = os.path.join(PROJECT_CONFIG_PATH, "environ.json")
AGENT_SAVE_PATH = os.path.join(PROJECT_CONFIG_PATH, "agent.json")
AGENT_CHECKPOINTS_PATH = os.path.join(PROJECT_CONFIG_PATH, "checkpoints")
EXTRAS_SAVE_PATH = os.path.join(PROJECT_CONFIG_PATH, "extras.json")
DOCS_EXTENSION = ".txt"
LOGGING_FILE_PATH = os.path.join(PROJECT_CONFIG_PATH, "logs", f"{datetime.now().timestamp()}.log")

IMPLEMENTATION_TRIES = 2
LLM_EXECUTOR_LOGGING = True
ANALYSIS_FILES_SIZE = 8
