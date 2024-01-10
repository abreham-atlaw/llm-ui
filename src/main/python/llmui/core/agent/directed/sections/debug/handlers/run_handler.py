from typing import Optional

from llmui.core.agent.directed.lib.handler import Handler, A, S
from llmui.core.agent.directed.lib.internal_state import InternalState
from llmui.core.environment import LLMUIState, LLMUIAction


class RunHandler(Handler[InternalState, None]):
	def _init_internal_state(self) -> InternalState:
		return InternalState()

	def _handle(self, state: LLMUIState, args: A) -> Optional[LLMUIAction]:
		print("[+]Running Program...")
		return LLMUIAction(
			"run",
			[state.root_path]
		)
