from typing import Optional

from llmui.core.agent.directed.lib.handler import Handler, A, S
from llmui.core.agent.directed.sections.debug.executors.error_extraction_executor import ErrorExtractionExecutor
from llmui.core.agent.directed.sections.debug.states.error_extraction_state import ErrorExtractionState
from llmui.core.environment import LLMUIState, LLMUIAction


class ErrorExtractionHandler(Handler[ErrorExtractionState, None]):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__executor = ErrorExtractionExecutor(self._llm)

	def _init_internal_state(self) -> ErrorExtractionState:
		return ErrorExtractionState()

	def handle(self, state: LLMUIState, args: None) -> Optional[LLMUIAction]:
		self.get_internal_state().extracted_message = self.__executor(state.output)
		return None