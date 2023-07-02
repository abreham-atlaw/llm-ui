import typing

from llmui.core.environment.action import LLMUIAction
from llmui.core.environment.action_executor import ActionExecutor


class WriteExecutor(ActionExecutor):
	def is_valid_action(self, action: LLMUIAction) -> bool:
		return action.command.startswith("write ")

	def __get_file_and_content(self, args: str) -> typing.Tuple[str, str]:
		splitted = args.split(" ")
		return splitted[0], " ".join(splitted[1:])

	def __write(self, file_path: str, content: str):
		with open(file_path, "w") as file:
			print(content, file=file)

	def execute(self, action: LLMUIAction) -> str:
		args = self._parse_arg(action)
		file_path, content = self.__get_file_and_content(args)
		self.__write(file_path, content)
		return f"Successfully wrote to {file_path}"
