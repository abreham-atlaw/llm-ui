import os

from llmui.core.agent.llmui_agent import LLMUIAgent
from llmui.core.environment import LLMUIEnvironment
from llmui.di import LLMProviders
from llmui.llm.console_llm import ConsoleLLM

if __name__ == "__main__":
	environment = LLMUIEnvironment("/home/abreham/Projects/TeamProjects/LLM-UI/temp/run")
	environment.start()
	agent = LLMUIAgent(LLMProviders.provide_default_llm())
	agent.set_environment(environment)
	agent.loop()
