import typing

from llmui.core.environment.action import LLMUIAction
from llmui.core.environment.action_executor import ActionExecutor


class ParentActionExecutor(ActionExecutor):

	def __init__(self, action_executors: typing.List[ActionExecutor]):
		self.__executors = action_executors

	def __find_executor(self, action: LLMUIAction) -> typing.Optional[ActionExecutor]:
		for executor in self.__executors:
			if executor.is_valid_action(action):
				return executor
		return None

	def is_valid_action(self, action: LLMUIAction) -> bool:
		return self.__find_executor(action) != False

	def execute(self, action: LLMUIAction) -> str:
		executor = self.__find_executor(action)
		if executor is None:
			raise ExecutorNotFoundException(action)
		return executor.execute(action)


class ExecutorNotFoundException(Exception):

	def __init__(self, action: LLMUIAction):
		super().__init__(f"Appropriate Executor not found for action {action}")
