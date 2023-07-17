import subprocess

from llmui.core.environment.action import LLMUIAction
from llmui.core.environment.action_executor import ActionExecutor


class RunExecutor(ActionExecutor):

	def is_valid_action(self, action: LLMUIAction) -> bool:
		return action.command == "run"

	def execute(self, action: LLMUIAction) -> str:
		command = action.args[0]
		p = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		response = ""
		while True:
			output = p.stdout.readline()
			if not output:
				break
			response = f"{output}\n"

		while True:
			err = p.stderr.readline()
			if not err:
				break
			response = f"{err}"

		return response
