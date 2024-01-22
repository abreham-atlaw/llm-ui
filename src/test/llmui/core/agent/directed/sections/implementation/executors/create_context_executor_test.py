import json
import unittest

from llmui.config import EXTRAS_SAVE_PATH, ENVIRON_PATH
from llmui.core.agent.directed.sections.implementation.executors.create_context_executor import CreateContextExecutor
from llmui.core.environment import LLMUIEnvironment
from llmui.di import LLMProviders
from llmui.di.utils_providers import UtilsProviders


class CreateContextExecutorTest(unittest.TestCase):

	def test_functionality(self):
		environment = LLMUIEnvironment(
			environ_file=ENVIRON_PATH
		)

		with open(EXTRAS_SAVE_PATH, "r") as file:
			extras = json.load(file)

		PROJECT_TASK = """
Phase 1: Data Layer Development

Task: Create models, serializers, request classes, and repositories for data retrieval and modification.

1. Create models for the following entities:
   - Product
   - BlogPost
   - JobOpening

2. Implement serializers to convert models to and from JSON format.

3. Define request classes for fetching data from the backend API:
   - GET /blog: Fetches all blog posts.
   - GET /blog/{id}: Fetches a specific blog post by ID.
   - GET /careers: Fetches all job openings.
   - GET /careers/{id}: Fetches a specific job opening by ID.

4. Develop repositories to manage data retrieval and modification:
   - Implement methods to fetch and store data for the following entities:
     - Product
     - BlogPost
     - JobOpening
   - Use the defined request classes to interact with the backend API for data retrieval.

Note: The models, serializers, request classes, and repositories should be developed in accordance with the project's backend API endpoints and the content source for each page.
"""
		TASK = "Create a file named Product.ts in the src/apps/core/data/models directory. Implement the Product model class with properties like id, name, and description."
		executor = CreateContextExecutor(LLMProviders.provide_default_llm())

		context = executor((
			environment.state.project_description,
			UtilsProviders.provide_documentation(extras["docs"]).search(TASK, num_results=1),
			PROJECT_TASK,
			TASK
		))

		self.assertIsNotNone(context)
