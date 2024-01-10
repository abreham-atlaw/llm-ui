from dataclasses import dataclass
from typing import Optional

import typing

from llmui.core.agent.directed.lib.handler import Handler, A, S
from llmui.core.agent.directed.sections.common.models import ProjectInfo
from llmui.core.agent.directed.sections.main.executors.phase_executor import PhaseExecutor
from llmui.core.agent.directed.sections.main.handlers.task_handler import TaskHandler, TaskHandlerArgs
from llmui.core.agent.directed.sections.main.states.phases_state import PhasesState
from llmui.core.agent.directed.sections.main.states.task_state import TaskStage
from llmui.core.environment import LLMUIState, LLMUIAction


@dataclass
class PhasesHandlerArgs:
	project_info: ProjectInfo
	debug: bool = True


class PhasesHandler(Handler[PhasesState, PhasesHandlerArgs]):

	INTERNAL_STATE_CLS = PhasesState

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__phases_breakdown_executor = PhaseExecutor(self._llm)
		self.__task_handler = TaskHandler(self._llm)

	def set_handlers(self, task):
		self.__task_handler = task

	def _init_internal_state(self) -> PhasesState:
		return PhasesState()

	def _handle(self, state: LLMUIState, args: PhasesHandlerArgs) -> Optional[LLMUIAction]:
		if self.internal_state.phases is None:
			print("[+]Breaking down phases...")
			self.internal_state.phases = self.__phases_breakdown_executor((state.project_description, args.project_info.task))
			return None
		if self.__task_handler.stage == TaskStage.done:
			if self.internal_state.phase_idx == len(self.internal_state.phases) - 1:
				self.internal_state.done = True
				return None
			self.internal_state.phase_idx += 1
			self.__task_handler.reset()
		return self.__task_handler.handle(state, TaskHandlerArgs(
			project_info=ProjectInfo(
				tech_stack=args.project_info.tech_stack,
				ignored_files=args.project_info.ignored_files,
				task=self.internal_state.current_phase
			),
			debug=args.debug
		))

	def export_config(self) -> typing.Dict[str, typing.Any]:
		return {
			"self": super().export_config(),
			"task": self.__task_handler.export_config()
		}

	@classmethod
	def load_config(cls, config: typing.Dict[str, typing.Any], *args, **kwargs) -> 'Handler':
		handler: PhasesHandler = super(PhasesHandler, cls).load_config(
			config["self"],
			*args,
			**kwargs
		)
		handler.set_handlers(
			task=TaskHandler.load_config(config["task"], *args, **kwargs)
		)
		return handler