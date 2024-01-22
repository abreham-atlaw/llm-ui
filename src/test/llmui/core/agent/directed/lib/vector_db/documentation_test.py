import json
import unittest

from llmui.config import EXTRAS_SAVE_PATH
from llmui.core.agent.directed.lib.vectordb.documentation import Documentation


class DocumentationTest(unittest.TestCase):

	def test_filter_for_task(self):
		with open(EXTRAS_SAVE_PATH, "r") as file:
			extras = json.load(file)
		documentation = Documentation(extras["docs"])

		result = documentation.search("""
Phase 1: Data Layer Development
1. Create models for entities such as Product, BlogPost, JobOpening, etc.
2. Implement serializers to convert models to and from JSON format.
3. Define request classes for fetching data from the backend API.
4. Develop repositories to manage data retrieval and modification.
""", num_results=2)

		self.assertIsNotNone(result)
