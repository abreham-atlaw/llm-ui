import typing
from abc import ABC, abstractmethod

from llmui.core.environment.action import LLMUIAction


class ActionExecutor(ABC):

	def _parse_arg(self, action: LLMUIAction) -> str:
		return " ".join(action.command.split(" ")[1:])

	@abstractmethod
	def is_valid_action(self, action: LLMUIAction) -> bool:
		pass

	@abstractmethod
	def execute(self, action: LLMUIAction) -> str:
		pass

	def __call__(self, *args, **kwargs):
		return self.execute(*args, **kwargs)
