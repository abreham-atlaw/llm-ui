import typing
from dataclasses import dataclass

from llmui.core.agent.directed.lib.internal_state import Stage, StagedInternalState
from llmui.core.agent.directed.sections.common.models import ProjectInfo


class InitStage(Stage):
	setup = 0
	analysis = 1
	fuse = 2


@dataclass
class InitState(StagedInternalState):
	project_info: typing.Optional[ProjectInfo] = None
	done: bool = False
