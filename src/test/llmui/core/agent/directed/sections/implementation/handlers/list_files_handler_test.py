import unittest

from llmui.config import ENVIRON_PATH, EXTRAS_SAVE_PATH
from llmui.core.agent.directed.sections.common.models import ProjectInfo
from llmui.core.agent.directed.sections.implementation.executors.list_files_executor import ListFilesExecutor
from llmui.core.agent.directed.sections.implementation.handlers.list_files_handler import ListFilesHandler, \
	ListFilesHandlerArgs
from llmui.core.environment import LLMUIState, LLMUIEnvironment
from llmui.di import LLMProviders

import json

from llmui.di.handler_providers import HandlerProviders


class ListFilesHandlerTest(unittest.TestCase):

	def test_functionality(self):
		environment = LLMUIEnvironment(
			environ_file=ENVIRON_PATH
		)

		with open(EXTRAS_SAVE_PATH, "r") as file:
			extras = json.load(file)

		handler = ListFilesHandler(LLMProviders.provide_default_llm())
		handler.handle(
			environment.state,
			ListFilesHandlerArgs(
				mode=ListFilesHandler.Mode.implementation,
				project_info=ProjectInfo(
					task="Phase 1: Data Layer Development\n\nTask 1: Create models for blog posts\n- Create a model for blog posts with the following fields: title (string), content (string), author (string), and date (datetime).\n\nTask 2: Implement serializers for blog posts\n- Implement serializers to convert blog post models to/from JSON.\n\nTask 3: Define requests for fetching blog posts\n- Define a request for fetching all blog posts from the backend API: `GET /blog`\n- Define a request for fetching a specific blog post by ID from the backend API: `GET /blog/{id}`\n\nTask 4: Create repositories for managing blog post data\n- Create repositories to manage blog post data from the backend API. These repositories should handle fetching all blog posts and fetching a specific blog post by ID.",
					tech_stack=extras["tech_stack"],
					ignored_files=extras["ignored_files"],
					docs=extras["docs"],
				),
			)
		)
		self.assertIsNotNone(handler.internal_state.tasks)

	def test_load_config(self):
		with open("/home/abreham/Projects/TeamProjects/LLM-UI/temp/config.json") as file:
			config = json.load(file)
		handler = ListFilesHandler.load_config(config, LLMProviders.provide_default_llm())
		self.assertIsNotNone(handler.get_internal_state().files)
