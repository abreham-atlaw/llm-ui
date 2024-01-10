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
				mode=ListFilesExecutor.Mode.implement,
				project_info=ProjectInfo(
					task="Task: Implementing the Structure of the Services Page\n\nDescription: In this phase, you will be responsible for implementing the structure of the Services page on the Orbit website. The Services page is an important section that showcases the various services offered by the company. It should follow the overall design theme of the website, featuring curved design elements and a visually pleasing user experience.\n\nPage-wise Details:\n\n1. Service Descriptions:\n   - Each service should be described within a card featuring a high border radius, giving it a pill-like shape.\n   - The card design should maintain the curved aesthetic in its design elements.\n   - The service descriptions should be visually appealing and easy to read.\n\n2. Case Studies:\n   - A carousel with curved edges should be implemented to showcase the case studies.\n   - Each case study should have a brief overview displayed within the carousel.\n   - The case study design should be consistent with the overall curved aesthetic of the website.\n\n3. Client Success Stories:\n   - A section should be created to showcase how the services provided by Orbit have helped clients achieve their goals.\n   - The client success stories should be visually appealing and presented in a way that highlights the positive impact of the services.\n\n4. FAQs:\n   - A section should be implemented to address common questions about the services offered by Orbit.\n   - The FAQs should be presented in a visually pleasing manner, maintaining the curved design elements of the website.\n\nBackend Endpoints:\n\n- GET /blog: Fetches all blog posts.\n- GET /blog/{id}: Fetches a specific blog post by ID.\n- POST /blog: Creates a new blog post (Admin only).\n- PUT /blog/{id}: Updates a specific blog post by ID (Admin only).\n- DELETE /blog/{id}: Deletes a specific blog post by ID (Admin only).\n- POST /contact: Submits the contact form.\n- GET /careers: Fetches all job openings.\n- GET /careers/{id}: Fetches a specific job opening by ID.\n- POST /careers: Creates a new job opening (Admin only).\n- PUT /careers/{id}: Updates a specific job opening by ID (Admin only).\n- DELETE /careers/{id}: Deletes a specific job opening by ID (Admin only).\n- POST /careers/{id}/apply: Submits the application form for a specific job opening.\n\nNote: The backend REST API for the Orbit website can be accessed at https://api.orbitwebsite.et/api.\n\nPlease ensure that the implemented structure of the Services page adheres to the provided project description and design guidelines.",
					tech_stack=extras["tech_stack"],
					ignored_files=extras["ignored_files"]
				),
				files_descriptions=HandlerProviders.provide_analysis_handler().internal_state.analysis
			)
		)
		self.assertIsNotNone(handler.internal_state.tasks)

	def test_load_config(self):
		with open("/home/abreham/Projects/TeamProjects/LLM-UI/temp/config.json") as file:
			config = json.load(file)
		handler = ListFilesHandler.load_config(config, LLMProviders.provide_default_llm())
		self.assertIsNotNone(handler.get_internal_state().files)
