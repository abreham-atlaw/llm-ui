from llmui.core.agent.directed_agent.stage import Stage


class HandlerNotFoundException(Exception):

	def __init__(self, stage: Stage):
		super().__init__(f"No handler found for stage {stage}")
