import typing
from abc import abstractmethod, ABC
from dataclasses import dataclass

from llmui.core.agent.directed_agent.stage import Stage
from llmui.core.agent.directed_agent.state import InternalState
from llmui.core.environment import LLMUIState, LLMUIAction, LLMUIEnvironment
from llmui.llm import LLM


@dataclass
class HandlerContext:
	project_description: typing.Optional[str]


class StageHandler(ABC):

	def __init__(self, llm: LLM):
		self.__llm = llm

	def _get_llm(self) -> LLM:
		return self.__llm

	@abstractmethod
	def handle(self, stage: Stage, internal_state: InternalState, state: LLMUIState, context: HandlerContext) -> typing.Optional[LLMUIAction]:
		pass
