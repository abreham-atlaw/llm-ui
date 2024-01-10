import unittest

from llmui.config import ENVIRON_PATH
from llmui.core.agent.directed.sections.common.models import ProjectInfo
from llmui.core.agent.directed.sections.init.handlers.fuse_task_handler import FuseTaskHandler, FuseTaskHandlerArgs
from llmui.core.environment import LLMUIEnvironment
from llmui.di import LLMProviders


class FuseTaskHandlerTest(unittest.TestCase):

	def test_functionality(self):
		environment = LLMUIEnvironment(
			environ_file=ENVIRON_PATH
		)

		handler = FuseTaskHandler(LLMProviders.provide_default_llm())

		handler._handle(
			environment.state,
			FuseTaskHandlerArgs(
				description=environment.state.project_description,
				task="Phase 1: Implementing the visual structure of the Services Page",
			)
		)

		self.assertIsNotNone(handler.internal_state.fused_task)
