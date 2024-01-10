import json
import os.path
import unittest

from llmui.config import EXTRAS_SAVE_PATH, ENVIRON_PATH
from llmui.core.agent.directed.sections.common.models import ProjectInfo
from llmui.core.agent.directed.sections.implementation.handlers.files_implementation_handler import \
	FilesImplementationHandler, FilesImplementationArgs
from llmui.core.environment import LLMUIState, LLMUIEnvironment
from llmui.di import LLMProviders


class FilesImplementationHandlerTest(unittest.TestCase):

	ROOT_PATH = "/home/abreham/Projects/TeamProjects/LLM-UI/temp/run"

	def test_functionality(self):
		environment = LLMUIEnvironment(
			environ_file=ENVIRON_PATH
		)

		handler = FilesImplementationHandler(LLMProviders.provide_default_llm())

		with open(EXTRAS_SAVE_PATH, "r") as file:
			extras = json.load(file)

		while not handler.get_internal_state().complete:
			action = handler.handle(
				environment.state,
				FilesImplementationArgs(
					project_info=ProjectInfo(
						task="Phase 1: Styling Header and Footer Components\n- Task 1: Apply the curved design aesthetic to the header component, incorporating a dynamic, full-screen banner with a curved lower boundary and interactive, circular icons with a high border radius for the key services.\n- Task 2: Apply the curved design aesthetic to the footer component, ensuring rounded corners for the footer elements and maintaining the overall sophisticated and modern look of the website.",
						tech_stack=extras["tech_stack"],
						ignored_files=extras["ignored_files"]
					),
					files_tasks={
						"orbit-website/src/components/Header.vue": "Implement the styling for the header component. Add necessary HTML elements and classes to structure the header. Apply appropriate styles using Tailwind CSS classes. Use Fontawesome icons for any icons needed in the header.",
						"orbit-website/src/components/Footer.vue": "Implement the styling for the footer component. Add necessary HTML elements and classes to structure the footer. Apply appropriate styles using Tailwind CSS classes. Use Fontawesome icons for any icons needed in the footer."
					},
				)
			)
			environment.do(action)

		self.assertTrue(handler.get_internal_state().complete)

	def test_load(self):
		handler = FilesImplementationHandler.load_handler("/home/abreham/Projects/TeamProjects/LLM-UI/temp/config1.json", LLMProviders.provide_default_llm())
		self.assertIsNotNone(handler.get_internal_state().implemented_files)
