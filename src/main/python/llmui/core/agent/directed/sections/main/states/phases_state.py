import typing
from dataclasses import dataclass

from llmui.core.agent.directed.lib.internal_state import StagedInternalState, InternalState


@dataclass
class PhasesState(InternalState):
	phases: typing.Optional[typing.List[str]] = None
	phase_idx: int = 0
	done: bool = False

	@property
	def current_phase(self) -> str:
		return self.phases[self.phase_idx]
