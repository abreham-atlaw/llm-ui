import unittest

from llmui.core.agent.directed.sections.common.models import ProjectInfo
from llmui.core.agent.directed.sections.init.handlers.setup_handler import SetupHandler, SetupHandlerArgs
from llmui.core.environment import LLMUIEnvironment
from llmui.di import LLMProviders


class SetupHandlerTest(unittest.TestCase):


	def test_functionality(self):
		environment = LLMUIEnvironment(
			cwd="/home/abreham/Projects/TeamProjects/LLM-UI/temp/projects/orbit/web",
			environ_file="/home/abreham/Projects/TeamProjects/LLM-UI/temp/projects/orbit/environ_state.json"
		)

		handler = SetupHandler(
			LLMProviders.provide_default_llm()
		)

		while not handler.internal_state.done:
			action = handler.handle(environment.state, SetupHandlerArgs(ProjectInfo(
				tech_stack=["Vue3", "Typescript", "Fedora"],
				description=environment.state.project_description
			)))
			environment.do(action)
