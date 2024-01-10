import unittest

from llmui.core.agent.directed.sections.init.handlers.init_handler import InitHandler, InitHandlerArgs
from llmui.core.environment import LLMUIEnvironment
from llmui.di import LLMProviders


class InitHandlerTest(unittest.TestCase):

	def test_functionality(self):
		environment = LLMUIEnvironment(
			environ_file="/home/abreham/Projects/TeamProjects/LLM-UI/temp/projects/orbit/environ.json"
		)
		# handler = InitHandler(LLMProviders.provide_default_llm())
		handler = InitHandler.load_handler("/home/abreham/Projects/TeamProjects/LLM-UI/temp/projects/orbit/init.json", LLMProviders.provide_default_llm())

		while not handler.internal_state.done:
			action = handler._handle(
				environment.state,
				InitHandlerArgs(
					tech_stack=["Vue3", "Typescript", "Fedora"],
					ignored_files=[
						"orbit-website/.vscode",
						"orbit-website/node_modules",
						"orbit-website/public",
						"orbit-website/src/assets",
						"orbit-website/package-lock.json",
						"orbit-website/package.json",
						"orbit-website/README.md",
						"orbit-website/.gitignore",
						"orbit-website/env.d.ts",
						"orbit-website/.eslintrc.cjs",
						"orbit-website/vite.config.ts",
						"orbit-website/tsconfig.node.json",
						"orbit-website/tsconfig.app.json",
						"orbit-website/tsconfig.json"
					],
					setup=False
				)
			)
			environment.do(action)
			handler.save("/home/abreham/Projects/TeamProjects/LLM-UI/temp/projects/orbit/init.json")
