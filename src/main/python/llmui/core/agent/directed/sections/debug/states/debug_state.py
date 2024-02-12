from dataclasses import dataclass

from llmui.core.agent.directed.lib.internal_state import Stage, StagedInternalState


class DebugStage(Stage):
	prep = 1
	run = 2
	check_results = 3
	check_stuck = 4
	user_help = 5
	error_extraction = 6
	cause_extraction = 7
	list_files = 8
	modify = 9
	done = 10


@dataclass
class DebugState(StagedInternalState):
	stage: DebugStage = DebugStage.prep
