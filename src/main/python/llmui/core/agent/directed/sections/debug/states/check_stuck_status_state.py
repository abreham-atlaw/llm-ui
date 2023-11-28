import typing
from dataclasses import dataclass

from llmui.core.agent.directed.lib.internal_state import InternalState


@dataclass
class CheckStuckStatusState(InternalState):
	is_stuck: typing.Optional[bool] = None
