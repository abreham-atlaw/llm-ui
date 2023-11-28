import os.path
import typing
from abc import ABC, abstractmethod

from llmui.core.environment.action import LLMUIAction


class ActionExecutor(ABC):

	def __init__(self, cwd=None):
		if cwd is None:
			cwd = os.path.abspath(".")
		self.__cwd = cwd

	@property
	def _cwd(self):
		return self._get_cwd()

	def _get_cwd(self) -> str:
		return self.__cwd

	def _get_relative_path(self, path) -> str:
		return os.path.join(self._get_cwd(), path)

	@abstractmethod
	def is_valid_action(self, action: LLMUIAction) -> bool:
		pass

	@abstractmethod
	def execute(self, action: LLMUIAction) -> str:
		pass

	def __call__(self, *args, **kwargs):
		return self.execute(*args, **kwargs)
