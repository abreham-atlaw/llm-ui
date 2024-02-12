from dataclasses import dataclass
from typing import Optional

from llmui.core.agent.directed.lib.handler import Handler, A, S
from llmui.core.agent.directed.lib.serializer import InternalStateSerializer
from llmui.core.agent.directed.sections.common.executors.format_executor import FormatExecutor
from llmui.core.agent.directed.sections.debug.executors.error_extraction_executor import ErrorExtractionExecutor
from llmui.core.agent.directed.sections.debug.serializers.error_extraction_state_serializer import \
	ErrorExtractionStateSerializer
from llmui.core.agent.directed.sections.debug.states.error_extraction_state import ErrorExtractionState
from llmui.core.environment import LLMUIState, LLMUIAction


@dataclass
class ErrorExtractionHandlerArgs:
	error: str


class ErrorExtractionHandler(Handler[ErrorExtractionState, None]):
	INTERNAL_STATE_CLS = ErrorExtractionState

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__executor = ErrorExtractionExecutor(self._llm)

	def _init_internal_state(self) -> ErrorExtractionState:
		return ErrorExtractionState()

	def _handle(self, state: LLMUIState, args: ErrorExtractionHandlerArgs) -> Optional[LLMUIAction]:
		print("[+]Extracting Error")
		self.internal_state.errors = self.__executor(args.error)
		return None

	@classmethod
	def _get_serializer(cls) -> InternalStateSerializer:
		return ErrorExtractionStateSerializer()

