import subprocess

from llmui.core.environment.action import LLMUIAction
from llmui.core.environment.action_executor import ActionExecutor


class RunExecutor(ActionExecutor):

	def is_valid_action(self, action: LLMUIAction) -> bool:
		return action.command == "run"

	def execute(self, action: LLMUIAction) -> str:
		command = action.args[0]
		try:
			return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
		except Exception as ex:
			return str(ex)
