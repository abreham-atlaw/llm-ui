import typing
from dataclasses import dataclass

from llmui.core.agent.directed.lib.internal_state import InternalState


@dataclass
class CheckResultsState(InternalState):
	passed: typing.Optional[bool] = None
