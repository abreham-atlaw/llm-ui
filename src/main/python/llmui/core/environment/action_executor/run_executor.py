import subprocess

from llmui.core.environment.action import LLMUIAction
from llmui.core.environment.action_executor import ActionExecutor


class RunExecutor(ActionExecutor):

	def is_valid_action(self, action: LLMUIAction) -> bool:
		return action.command.startswith("run ")

	def execute(self, action: LLMUIAction) -> str:
		command = self._parse_arg(action)
		try:
			return subprocess.check_output(command)
		except Exception as ex:
			return str(ex)
