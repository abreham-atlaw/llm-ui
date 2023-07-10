import typing

from llmui.core.environment.action import LLMUIAction
from llmui.core.environment.action_executor import ActionExecutor


class WriteExecutor(ActionExecutor):
	def is_valid_action(self, action: LLMUIAction) -> bool:
		return action.command == "write"

	def __write(self, file_path: str, content: str):
		with open(file_path, "w") as file:
			print(content, file=file)

	def execute(self, action: LLMUIAction) -> str:
		file_path, content = action.args
		self.__write(file_path, content)
		return f"Successfully wrote to {file_path}"
