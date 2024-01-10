import json
import unittest

from llmui.config import ENVIRON_PATH, AGENT_SAVE_PATH, EXTRAS_SAVE_PATH
from llmui.core.agent.directed.sections.common.models import ProjectInfo
from llmui.core.agent.directed.sections.main.handlers.phases_handler import PhasesHandler, PhasesHandlerArgs
from llmui.core.environment import LLMUIEnvironment
from llmui.di import LLMProviders


class PhasesHandlerTest(unittest.TestCase):

	def test_functionality(self):
		environment = LLMUIEnvironment(
			environ_file=ENVIRON_PATH
		)

		# handler = PhasesHandler(LLMProviders.provide_default_llm())
		handler = PhasesHandler.load_handler(AGENT_SAVE_PATH, LLMProviders.provide_default_llm())

		with open(EXTRAS_SAVE_PATH, "r") as file:
			extras = json.load(file)

		while not handler.internal_state.done:
			action = handler.handle(
				environment.state,
				PhasesHandlerArgs(
					debug=True,
					project_info=ProjectInfo(
						task=environment.state.task,
						tech_stack=extras["tech_stack"],
						ignored_files=extras["ignored_files"]
					)
				)
			)
			handler.save(AGENT_SAVE_PATH)
			environment.do(action)
