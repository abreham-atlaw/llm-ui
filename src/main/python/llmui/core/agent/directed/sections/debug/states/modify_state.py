import typing
from dataclasses import dataclass, field

from llmui.core.agent.directed.lib.internal_state import InternalState


@dataclass
class ModifyState(InternalState):
	contents: typing.Optional[typing.Dict[str, str]] = None
	implemented_files: typing.List[str] = field(default_factory=lambda: [])
	done: bool = False
