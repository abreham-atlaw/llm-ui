import unittest

from llmui.core.agent.directed.sections.debug.executors.list_files_executor import ListFilesExecutor
from llmui.core.agent.directed.sections.implementation.handlers.list_files_handler import ListFilesHandler, \
	ListFilesHandlerArgs
from llmui.core.environment import LLMUIState, LLMUIEnvironment
from llmui.di import LLMProviders

import json


class ListFilesHandlerTest(unittest.TestCase):

	def test_functionality(self):
		environment = LLMUIEnvironment(
			cwd="/home/abreham/Projects/TeamProjects/LLM-UI/temp/projects/orbit/web",
			environ_file="/home/abreham/Projects/TeamProjects/LLM-UI/temp/projects/orbit/environ_state.json"
		)

		handler = ListFilesHandler(LLMProviders.provide_default_llm())
		handler.handle(
			environment.state,
			ListFilesHandlerArgs(
				mode=ListFilesExecutor.Mode.implement,
				files_descriptions=
			)
		)
		config = handler.export_config()
		self.assertIsNotNone(handler.get_internal_state().files)

	def test_load_config(self):
		with open("/home/abreham/Projects/TeamProjects/LLM-UI/temp/config.json") as file:
			config = json.load(file)
		handler = ListFilesHandler.load_config(config, LLMProviders.provide_default_llm())
		self.assertIsNotNone(handler.get_internal_state().files)
