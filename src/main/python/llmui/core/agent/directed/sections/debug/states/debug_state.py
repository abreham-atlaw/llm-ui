from dataclasses import dataclass

from llmui.core.agent.directed.lib.internal_state import Stage, StagedInternalState


class DebugStage(Stage):
	prep = 1
	run = 2
	error_extraction = 3
	list_files = 4
	modify = 5
	done = 6


@dataclass
class DebugState(StagedInternalState):
	stage: DebugStage = DebugStage.prep
