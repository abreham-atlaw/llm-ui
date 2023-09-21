import typing
from abc import abstractmethod

from llmui.llm import LLM

I = typing.TypeVar('I')
O = typing.TypeVar('O')


class LLMExecutor(typing.Generic[I, O]):

	def __init__(self, llm: LLM):
		self._llm = llm

	@abstractmethod
	def _prepare_prompt(self, arg: I) -> str:
		pass

	@abstractmethod
	def _prepare_output(self, output: str, arg: I) -> O:
		pass

	def call(self, arg: I) -> O:
		prompt = self._prepare_prompt(arg)
		llm_output = self._llm.chat(prompt)
		return self._prepare_output(llm_output, arg)

	def __call__(self, arg: I):
		return self.call(arg)
