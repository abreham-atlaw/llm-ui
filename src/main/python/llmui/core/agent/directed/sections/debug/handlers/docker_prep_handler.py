from typing import Optional

from llmui.core.agent.directed.lib.handler import Handler, A, S
from llmui.core.agent.directed.sections.debug.executors.docker_prep_executor import DockerPrepExecutor
from llmui.core.agent.directed.sections.debug.states.docker_prep_state import DockerPrepState
from llmui.core.environment import LLMUIState, LLMUIAction


class DockerPrepHandler(Handler[DockerPrepState, None]):

	INTERNAL_STATE_CLS = DockerPrepState

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__executor = DockerPrepExecutor(self._llm)

	def _init_internal_state(self) -> DockerPrepState:
		return DockerPrepState()

	def handle(self, state: LLMUIState, args: None) -> Optional[LLMUIAction]:
		if "Dockerfile" in state.files:
			self.get_internal_state().complete = True
			return None
		response = self.__executor.call(state.root_path)
		self.get_internal_state().complete = True
		return LLMUIAction(
			"write",
			[
				"Dockerfile",
				response
			]
		)
