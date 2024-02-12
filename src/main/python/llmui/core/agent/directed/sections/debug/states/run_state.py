import typing
from dataclasses import dataclass

from llmui.core.agent.directed.lib.internal_state import InternalState


@dataclass
class RunState(InternalState):
	output: typing.Optional[str] = None
	run: bool = False

	@property
	def done(self):
		return self.output is not None
