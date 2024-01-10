import typing
from dataclasses import dataclass
from typing import Optional

from llmui.core.agent.directed.lib.handler import Handler
from llmui.core.agent.directed.sections.common.models import ProjectInfo
from llmui.core.agent.directed.sections.debug.executors.docker_prep_executor import DockerPrepExecutor
from llmui.core.agent.directed.sections.debug.states.docker_prep_state import DockerPrepState
from llmui.core.environment import LLMUIState, LLMUIAction


@dataclass
class DockerPrepHandlerArgs:
	project_info: ProjectInfo


class DockerPrepHandler(Handler[DockerPrepState, DockerPrepHandlerArgs]):

	INTERNAL_STATE_CLS = DockerPrepState

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__executor = DockerPrepExecutor(self._llm)

	def _init_internal_state(self) -> DockerPrepState:
		return DockerPrepState()

	def _handle(self, state: LLMUIState, args: DockerPrepHandlerArgs) -> Optional[LLMUIAction]:
		if "Dockerfile" in state.files:
			self.internal_state.complete = True
			return None
		print("[+]Preparing Debug...")
		response = self.__executor((state.files, args.project_info.tech_stack, args.project_info.ignored_files))
		self.internal_state.complete = True
		return LLMUIAction(
			"write",
			[
				"Dockerfile",
				response
			]
		)
