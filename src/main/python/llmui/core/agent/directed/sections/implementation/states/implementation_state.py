from llmui.core.agent.directed.lib.internal_state import Stage, StagedInternalState


class ImplementationStage(Stage):
	list_files = 0
	dependencies = 1
	implement_files = 2
	done = 3


class ImplementationState(StagedInternalState):
	pass
