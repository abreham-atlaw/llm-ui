import typing
from abc import abstractmethod

from datetime import datetime

from lib.utils.logger import Logger
from llmui.config import LLM_EXECUTOR_LOGGING
from llmui.llm import LLM

I = typing.TypeVar('I')
O = typing.TypeVar('O')


class LLMExecutor(typing.Generic[I, O]):

	def __init__(self, llm: LLM, logging=LLM_EXECUTOR_LOGGING):
		self._llm = llm
		self.__logging = logging

	@abstractmethod
	def _prepare_prompt(self, arg: I) -> str:
		pass

	@abstractmethod
	def _prepare_output(self, output: str, arg: I) -> O:
		pass

	def __log(self, prompt: str, llm_output: str, final_output: str):
		Logger.info(f"""\n\n\n{'-'*20}
[{datetime.now()}] {self.__class__.__name__}:

PROMPT:
{'_'*10}
{prompt}
{'_'*10}

LLM OUTPUT:
{'_'*10}
{llm_output}
{'_'*10}

FINAL OUTPUT:
{'_'*10}
{final_output}
{'_'*10}
{'-'*20}\n\n\n""")

	def call(self, arg: I) -> O:
		prompt = self._prepare_prompt(arg)
		llm_output = self._llm.chat(prompt)
		final_output = self._prepare_output(llm_output, arg)
		if self.__logging:
			self.__log(prompt, llm_output,final_output)
		return final_output

	def __call__(self, arg: I):
		return self.call(arg)
