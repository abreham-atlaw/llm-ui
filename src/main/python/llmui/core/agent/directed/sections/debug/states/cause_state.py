import typing
from dataclasses import dataclass

from llmui.core.agent.directed.lib.internal_state import InternalState


@dataclass
class CauseState(InternalState):
	relevant_files: typing.Optional[typing.List[str]] = None
	cause: typing.Optional[str] = None
	done: bool = False
