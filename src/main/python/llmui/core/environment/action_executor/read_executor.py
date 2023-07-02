from llmui.core.environment.action import LLMUIAction
from llmui.core.environment.action_executor import ActionExecutor


class ReadExecutor(ActionExecutor):

	def is_valid_action(self, action: LLMUIAction) -> bool:
		return action.command.startswith("read ")

	@staticmethod
	def __read(file_path: str) -> str:
		with open(file_path) as file:
			content = file.read()
		return content

	def execute(self, action: LLMUIAction) -> str:
		file_path = self._parse_arg(action)
		return self.__read(file_path)
