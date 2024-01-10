import typing
from dataclasses import dataclass

from llmui.core.agent.directed.lib.internal_state import Stage, StagedInternalState


class ImplementationStage(Stage):
	list_files = 0
	implement_files = 1
	done = 2


@dataclass
class ImplementationState(StagedInternalState):
	implemented_files: typing.Optional[typing.List[str]] = None
