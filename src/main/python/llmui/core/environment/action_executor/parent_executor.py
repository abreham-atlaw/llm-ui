import typing

from llmui.core.environment.action import LLMUIAction
from llmui.core.environment.action_executor import ActionExecutor


class ParentActionExecutor(ActionExecutor):

	def __init__(self, action_executors: typing.List[ActionExecutor], *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__executors = action_executors

	def __find_executor(self, action: LLMUIAction) -> typing.Optional[ActionExecutor]:
		for executor in self.__executors:
			if executor.is_valid_action(action):
				return executor
		return None

	def is_valid_action(self, action: LLMUIAction) -> bool:
		return action is None or self.__find_executor(action) is not False

	def execute(self, action: typing.Optional[LLMUIAction]) -> str:
		if action is None:
			return ""
		executor = self.__find_executor(action)
		if executor is None:
			raise ExecutorNotFoundException(action)
		try:
			return executor.execute(action)
		except Exception as ex:
			return f"Error: {ex}"


class ExecutorNotFoundException(Exception):

	def __init__(self, action: LLMUIAction):
		super().__init__(f"Appropriate Executor not found for action {action}")
