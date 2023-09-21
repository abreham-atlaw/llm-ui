from dataclasses import dataclass

from llmui.core.agent.directed.lib.internal_state import InternalState


@dataclass
class PrepState(InternalState):
	docker: bool
	complete: bool
