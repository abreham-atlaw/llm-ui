from typing import Optional

from llmui.core.agent.directed.lib.handler import Handler, A, S
from llmui.core.agent.directed.sections.debug.executors.check_results_executor import CheckResultsExecutor
from llmui.core.agent.directed.sections.debug.states.check_results_state import CheckResultsState
from llmui.core.environment import LLMUIState, LLMUIAction


class CheckResultsHandler(Handler[CheckResultsState, None]):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__executor = CheckResultsExecutor(self._llm)

	def _init_internal_state(self) -> CheckResultsState:
		return CheckResultsState()

	def _handle(self, state: LLMUIState, args: None) -> Optional[LLMUIAction]:
		print("[+]Checking Results")
		self.internal_state.passed = self.__executor(state.output)
		return None
