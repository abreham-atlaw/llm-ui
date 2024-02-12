from typing import Optional

from llmui.core.agent.directed.lib.handler import Handler, A, S
from llmui.core.agent.directed.lib.internal_state import InternalState
from llmui.core.agent.directed.sections.debug.states.run_state import RunState
from llmui.core.environment import LLMUIState, LLMUIAction


class RunHandler(Handler[RunState, None]):

	INTERNAL_STATE_CLS = RunState

	def _init_internal_state(self) -> RunState:
		return RunState()

	def _handle(self, state: LLMUIState, args: None) -> Optional[LLMUIAction]:
		if self.internal_state.run and state.output != "":
			self.internal_state.output = state.output
			return None

		print("[+]Running Program...")
		self.internal_state.run = True
		return LLMUIAction(
			"run",
			[state.root_path]
		)
