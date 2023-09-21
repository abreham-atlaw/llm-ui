import typing
from abc import ABC, abstractmethod
from typing import Generic

from llmui.llm import LLM

T = typing.TypeVar("T")


class ResponseParser(ABC, Generic[T]):

	@abstractmethod
	def parse(self, text: str) -> T:
		pass

	def __call__(self, text: str) -> T:
		return self.parse(text)


class LLMResponseParser(ResponseParser, ABC, Generic[T]):

	def __init__(self, llm: LLM):
		self._llm = llm
