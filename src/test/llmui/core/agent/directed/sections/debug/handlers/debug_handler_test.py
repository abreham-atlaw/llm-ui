import json
import unittest
import os

from lib.runtime.runners.docker_runner import DockerRunner
from llmui.config import ENVIRON_PATH, EXTRAS_SAVE_PATH, PROJECT_CONFIG_PATH
from llmui.core.agent.directed.sections.common.models import ProjectInfo
from llmui.core.agent.directed.sections.debug.handlers.debug_handler import DebugHandler, DebugHandlerArgs
from llmui.core.agent.directed.sections.debug.handlers.modify_handler import ModifyHandlerArgs
from llmui.core.agent.directed.sections.debug.states.debug_state import DebugStage
from llmui.core.environment import LLMUIState, LLMUIEnvironment
from llmui.di import LLMProviders


class DebugHandlerTest(unittest.TestCase):

	def test_functionality(self):
		environment = LLMUIEnvironment(
			environ_file=ENVIRON_PATH
		)

		with open(EXTRAS_SAVE_PATH, "r") as file:
			extras = json.load(file)

		handler = DebugHandler(LLMProviders.provide_default_llm())
		# handler = DebugHandler.load_handler(os.path.join(PROJECT_CONFIG_PATH, "debug.json"), LLMProviders.provide_default_llm())

		while handler.get_internal_state().stage != DebugStage.done:
			action = handler._handle(
				environment.state,
				DebugHandlerArgs(
					project_info=ProjectInfo(
						task="Phase 1: Header and Footer Components\n\nIn this phase, you will be responsible for creating the header and footer components for the Orbit website. The header component should have a visually striking design that aligns with the overall theme of the website. It should feature a dark background with curved edges, giving it a soft and approachable aesthetic. The primary color used in the header should be orange, symbolizing the company's creativity and dynamism.\n\nThe header component should include the company logo, a navigation menu with links to different pages of the website, and a search bar. The logo should be prominently displayed and positioned at the top left corner of the header. The navigation menu should be horizontally aligned and have a button-like appearance, with circular icons for each key service. The search bar should be positioned on the right side of the header.\n\nThe footer component should also have a dark background with curved edges, maintaining consistency with the overall design of the website. It should include links to important pages such as the Home, About Us, Services, Projects, Blog, Contact Us, and Careers pages. Additionally, the footer should feature social media icons for easy access to the company's social media profiles.\n\nBoth the header and footer components should be responsive and adapt to different screen sizes. They should be visually appealing and provide a seamless user experience.",
						tech_stack=extras["tech_stack"],
						ignored_files=extras["ignored_files"]
					)
				)
			)
			handler.save(os.path.join(PROJECT_CONFIG_PATH, "debug.json"))
			environment.do(action)

		self.assertTrue(handler.get_internal_state().stage == DebugStage.done)
