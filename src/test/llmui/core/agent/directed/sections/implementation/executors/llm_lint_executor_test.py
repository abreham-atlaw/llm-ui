import json
import unittest

from llmui.config import ENVIRON_PATH, EXTRAS_SAVE_PATH
from llmui.core.agent.directed.sections.implementation.executors.llm_lint_executor import LLMLintExecutor
from llmui.core.environment import LLMUIEnvironment
from llmui.di import LLMProviders


class LLMLintExecutorTest(unittest.TestCase):

	def test_negative(self):
		environment = LLMUIEnvironment(
			environ_file=ENVIRON_PATH
		)

		with open(EXTRAS_SAVE_PATH, "r") as file:
			extras = json.load(file)

		executor = LLMLintExecutor(LLMProviders.provide_default_llm())
		filename = "src/views/Services.vue"
		errors = executor((
			filename,
			environment.state.read_content(filename),
			extras["tech_stack"]
		))

		self.assertEqual(errors, [])

	def test_positive(self):
		environment = LLMUIEnvironment(
			environ_file=ENVIRON_PATH
		)

		with open(EXTRAS_SAVE_PATH, "r") as file:
			extras = json.load(file)

		executor = LLMLintExecutor(LLMProviders.provide_default_llm())
		filename = "src/views/Services.vue"
		errors = executor((
			filename,
			environment.state.read_content(filename),
			extras["tech_stack"]
		))

		self.assertNotEqual(errors, [])
