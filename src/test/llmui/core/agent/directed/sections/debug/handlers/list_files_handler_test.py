import unittest

import os

from llmui.core.agent.directed.sections.debug.handlers.list_files_handler import ListFilesHandler
from llmui.core.environment import LLMUIState
from llmui.di import LLMProviders


class ListFilesHandlerTest(unittest.TestCase):
	ROOT_PATH = "/home/abreham/Projects/TeamProjects/LLM-UI/temp/run"

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

	@staticmethod
	def __create_dir(path: str):
		os.makedirs(os.path.dirname(path), exist_ok=True)

	def test_functionality(self):
		state = LLMUIState(
			action_stack=[],
			output="""Command 'None' in image '1695176824.182712' returned non-zero exit status 1: b'E\n======================================================================\nERROR: test_app (unittest.loader._FailedTest)\n----------------------------------------------------------------------\nImportError: Failed to import test module: test_app\nTraceback (most recent call last):\n  File "/usr/local/lib/python3.9/unittest/loader.py", line 436, in _find_test_path\n    module = self._get_module_from_name(name)\n  File "/usr/local/lib/python3.9/unittest/loader.py", line 377, in _get_module_from_name\n    __import__(name)\n  File "/app/tests/test_app.py", line 2, in <module>\n    from app import app, db\n  File "/app/app.py", line 1, in <module>\n    from flask import Flask\nModuleNotFoundError: No module named \'flask\'\n----------------------------------------------------------------------\nRan 1 test in 0.001s\nFAILED (errors=1)\n'""",
			read_content=self.read_content,
			root_path=self.ROOT_PATH,
			project_description="""
The app is a flask rest-api backend for a simple todo list.
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
		handler = ListFilesHandler(LLMProviders.provide_console_llm())
		handler.handle(
			state,
			None
		)
		self.assertGreater(len(handler.get_internal_state().files), 0)

