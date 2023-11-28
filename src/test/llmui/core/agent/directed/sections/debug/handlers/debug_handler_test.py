import unittest
import os

from lib.runtime.runners.docker_runner import DockerRunner
from llmui.core.agent.directed.sections.common.models import ProjectInfo
from llmui.core.agent.directed.sections.debug.handlers.debug_handler import DebugHandler, DebugHandlerArgs
from llmui.core.agent.directed.sections.debug.handlers.modify_handler import ModifyHandlerArgs
from llmui.core.agent.directed.sections.debug.states.debug_state import DebugStage
from llmui.core.environment import LLMUIState
from llmui.di import LLMProviders


class DebugHandlerTest(unittest.TestCase):

	ROOT_PATH = "/home/abreham/Projects/TeamProjects/LLM-UI/temp/run"

	def setUp(self) -> None:
		self.__runner = DockerRunner()

	def read_content(self, file) -> str:
		file = os.path.join(self.ROOT_PATH, file)
		if not os.path.exists(file):
			return ""
		with open(file, "r") as file:
			content = file.read()
			return content

	def __write(self, file_path: str, content: str):
		self.__create_dir(file_path)
		with open(file_path, "w") as file:
			print(content, file=file)

	def __run(self, path) -> str:
		return self.__runner.run(path)

	@staticmethod
	def __create_dir(path: str):
		os.makedirs(os.path.dirname(path), exist_ok=True)

	def test_functionality(self):
		state = LLMUIState(
			action_stack=[],
			outputs=[],
			read_content=self.read_content,
			root_path=self.ROOT_PATH,
			project_description="""
The app is a flask rest-api backend for a simple todo list. The unittest is done using pytest
The app will have the following features:

	Users can add new todo items.
	Users can edit existing todo items.
	Users can delete todo items.
	Users can mark todo items as completed.
	Users can view a list of all their todo items.

The following are the required endpoints for the app:

	/: This is the home page of the app. It will display a list of all the todo items for the current user.
	/add: This endpoint allows users to add new todo items.
	/edit/<int:todo_id>: This endpoint allows users to edit existing todo items. The todo_id parameter is the ID of the todo item to be edited.
	/delete/<int:todo_id>: This endpoint allows users to delete existing todo items. The todo_id parameter is the ID of the todo item to be deleted.
	/complete/<int:todo_id>: This endpoint allows users to mark a todo item as completed. The todo_id parameter is the ID of the todo item to be marked as completed.
"""
		)

		handler = DebugHandler(LLMProviders.provide_console_llm())

		while handler.get_internal_state().stage != DebugStage.done:
			action = handler.handle(
				state,
				DebugHandlerArgs(
					project_info=ProjectInfo(
						description=state.project_description,
						tech_stack=["python", "flask", "unittest"]
					)
				)
			)
			if action is not None:
				if action.command == "write":
					self.__write(os.path.join(self.ROOT_PATH, action.args[0]), action.args[1])
				elif action.command == "run":
					state.outputs.append(self.__run(state.root_path))

		self.assertTrue(handler.get_internal_state().stage == DebugStage.done)
