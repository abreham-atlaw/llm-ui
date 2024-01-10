import json
import unittest

from llmui.config import ENVIRON_PATH, EXTRAS_SAVE_PATH, ANALYSIS_SAVE_PATH
from llmui.core.agent.directed.sections.init.handlers.analysis_handler import AnalysisHandler, \
	AnalysisHandlerArgs
from llmui.core.environment import LLMUIEnvironment
from llmui.di import LLMProviders
from llmui.di.handler_providers import HandlerProviders


class AnalyzeProjectHandlerTest(unittest.TestCase):

	def test_functionality(self):
		environment = LLMUIEnvironment(
			environ_file=ENVIRON_PATH
		)
		handler = HandlerProviders.provide_analysis_handler()
		# handler = AnalysisHandler(LLMProviders.provide_default_llm())

		with open(EXTRAS_SAVE_PATH, "r") as file:
			extras = json.load(file)

		handler.handle(
			environment.state,
			AnalysisHandlerArgs(
				ignored_files=extras["ignored_files"]
			)
		)

		handler.save(ANALYSIS_SAVE_PATH)

		self.assertIsNotNone(handler.internal_state.analysis)


