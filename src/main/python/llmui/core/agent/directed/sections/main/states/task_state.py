from dataclasses import dataclass

from llmui.core.agent.directed.lib.internal_state import InternalState, Stage, StagedInternalState


class TaskStage(Stage):
	init = 0
	implementation = 1
	test_implementation = 2
	debug = 3
	done = 4


@dataclass
class TaskState(StagedInternalState):
	pass
