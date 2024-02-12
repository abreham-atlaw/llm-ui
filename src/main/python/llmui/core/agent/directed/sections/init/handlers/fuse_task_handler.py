from dataclasses import dataclass
from typing import Optional

from llmui.core.agent.directed.lib.handler import Handler, A, S
from llmui.core.agent.directed.sections.common.models import ProjectInfo
from llmui.core.agent.directed.sections.init.executors.fuse_task_executor import FuseTaskExecutor
from llmui.core.agent.directed.sections.init.states.fuse_task_state import FuseTaskState
from llmui.core.environment import LLMUIState, LLMUIAction
from llmui.di.utils_providers import UtilsProviders


@dataclass
class FuseTaskHandlerArgs:
	project_info: ProjectInfo
	description: str


class FuseTaskHandler(Handler[FuseTaskState, FuseTaskHandlerArgs]):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__executor = FuseTaskExecutor(self._llm)

	def _init_internal_state(self) -> FuseTaskState:
		return FuseTaskState()

	def _handle(self, state: LLMUIState, args: FuseTaskHandlerArgs) -> Optional[LLMUIAction]:
		print("[+]Fusing Task...")
		self.internal_state.fused_task = self.__executor((
			args.description,
			args.project_info.task,
			UtilsProviders.provide_documentation(args.project_info.docs).search(args.project_info.task, num_results=3)
		))
		return None
