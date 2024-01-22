import typing
from dataclasses import dataclass

from llmui.core.agent.directed.lib.internal_state import Stage, StagedInternalState
from llmui.core.agent.directed.sections.common.models import ProjectInfo


class ImplementationStage(Stage):
	list_files = 0
	implement_files = 1
	done = 2


@dataclass
class ImplementationState(StagedInternalState):
	project_task: str = None
	implemented_files: typing.Optional[typing.List[str]] = None
