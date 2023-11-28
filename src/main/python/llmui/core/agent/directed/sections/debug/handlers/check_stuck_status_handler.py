from typing import Optional

from llmui.core.agent.directed.lib.handler import Handler, A, S
from llmui.core.agent.directed.sections.debug.executors.check_stuck_status_executor import CheckStuckStatusExecutor
from llmui.core.agent.directed.sections.debug.states.check_stuck_status_state import CheckStuckStatusState
from llmui.core.environment import LLMUIState, LLMUIAction


class CheckStuckStatusHandler(Handler[CheckStuckStatusState, None]):

	def __init__(self, *args, lookback=3, **kwargs):
		super().__init__(*args, **kwargs)
		self.__executor = CheckStuckStatusExecutor(self._llm)
		self.__lookback = lookback

	def _init_internal_state(self) -> CheckStuckStatusState:
		return CheckStuckStatusState()

	def handle(self, state: LLMUIState, args: None) -> Optional[LLMUIAction]:
		if len(state.outputs) < self.__lookback:
			self.get_internal_state().is_stuck = False
			return
		self.get_internal_state().is_stuck = self.__executor(state.outputs[-self.__lookback:])
		return None
