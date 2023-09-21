import subprocess

from lib.runtime.runners.docker_runner import DockerRunner
from llmui.core.environment.action import LLMUIAction
from llmui.core.environment.action_executor import ActionExecutor


class RunExecutor(ActionExecutor):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__runner = DockerRunner()

	def is_valid_action(self, action: LLMUIAction) -> bool:
		return action.command == "run"

	def execute(self, action: LLMUIAction) -> str:
		return self.__runner.run(self._get_cwd())

