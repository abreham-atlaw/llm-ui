import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

LOGGING = True
LOGGING_PID = True
LOGGING_CONSOLE = False
LOGGING_FILE_PATH = os.path.join(BASE_DIR, "out.log")

OPENAI_KEY = "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"

LLM_TEMPERATURE = 0.01


GAI_URL = "https://llmchat-server.vercel.app/api/"

PROJECT_PATH = os.path.abspath("/home/abreham/Projects/TeamProjects/LLM-UI/temp/projects/orbit/web/orbit-website")
PROJECT_CONFIG_PATH = os.path.join(PROJECT_PATH, ".cop")
ANALYSIS_SAVE_PATH = os.path.join(PROJECT_CONFIG_PATH, "analysis.json")
ENVIRON_PATH = os.path.join(PROJECT_CONFIG_PATH, "environ.json")
AGENT_SAVE_PATH = os.path.join(PROJECT_CONFIG_PATH, "agent.json")
EXTRAS_SAVE_PATH = os.path.join(PROJECT_CONFIG_PATH, "extras.json")


IMPLEMENTATION_TRIES = 2
LLM_EXECUTOR_LOGGING = True
