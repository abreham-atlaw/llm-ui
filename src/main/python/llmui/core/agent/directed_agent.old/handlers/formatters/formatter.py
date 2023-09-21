from abc import abstractmethod, ABC

from llmui.llm import LLM


class Formatter(ABC):

	@abstractmethod
	def format(self, *args, **kwargs) -> str:
		pass

	def __call__(self, *args, **kwargs):
		return self.format(*args, **kwargs)


class LLMFormatter(Formatter, ABC):

	def __init__(self, llm: LLM):
		self._llm = llm
