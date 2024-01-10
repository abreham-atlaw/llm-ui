import unittest

from llmui.core.agent.directed.sections.init.executors.analyze_file_executor import AnalyzeFileExecutor
from llmui.core.environment import LLMUIEnvironment
from llmui.di import LLMProviders


class AnalyzeFileExecutorTest(unittest.TestCase):

	def test_functionality(self):
		environment = LLMUIEnvironment(
			environ_file="/home/abreham/Projects/TeamProjects/LLM-UI/temp/projects/orbit/environ.json"
		)

		executor = AnalyzeFileExecutor(LLMProviders.provide_console_llm())
		analysis = executor((
			"orbit-website/src/views/HomeView.vue",
			environment.state.read_content
		))

		self.assertIsNotNone(analysis)
