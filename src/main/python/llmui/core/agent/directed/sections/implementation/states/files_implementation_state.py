import typing

from dataclasses import dataclass, field

from llmui.core.agent.directed.lib.internal_state import InternalState


@dataclass
class FilesImplementationState(InternalState):

	implemented_files: typing.List[str] = field(default_factory=lambda:[])
	complete: bool = False
