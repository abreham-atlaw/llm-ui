import typing

import os

from llmui.core.environment.action import LLMUIAction
from llmui.core.environment.action_executor import ActionExecutor


class WriteExecutor(ActionExecutor):
	def is_valid_action(self, action: LLMUIAction) -> bool:
		return action.command == "write"

	def __create_dir(self, path: str):
		os.makedirs(path, exist_ok=True)

	def __write(self, file_path: str, content: str):
		parent = os.path.dirname(file_path)
		if parent == "":
			parent = "./"
		if not os.path.exists(parent):
			self.__create_dir(parent)
		with open(file_path, "w") as file:
			print(content, file=file)

	def execute(self, action: LLMUIAction) -> str:
		file_path, content = action.args
		self.__write(file_path, content)
		return f"Successfully wrote to {file_path}"
