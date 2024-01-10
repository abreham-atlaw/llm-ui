import typing
from dataclasses import dataclass

from llmui.core.agent.directed.lib.internal_state import InternalState


@dataclass
class FuseTaskState(InternalState):

	fused_task: typing.Optional[str] = None
