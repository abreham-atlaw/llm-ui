import os.path

from llmui.core.environment.action import LLMUIAction
from llmui.core.environment.action_executor import ActionExecutor


class ReadExecutor(ActionExecutor):

	def is_valid_action(self, action: LLMUIAction) -> bool:
		return action.command == "read"

	@staticmethod
	def __read(file_path: str) -> str:
		if file_path.startswith("/"):
			file_path = file_path[1:]
		if not os.path.exists(file_path):
			return ""
		with open(file_path) as file:
			content = file.read()
		return content

	def execute(self, action: LLMUIAction) -> str:
		file_path = action.args[0]
		return self.__read(file_path)
