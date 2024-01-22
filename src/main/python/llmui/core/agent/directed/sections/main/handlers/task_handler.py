import typing
from dataclasses import dataclass
from typing import Optional

from llmui.core.agent.directed.lib.handler import Handler, A, S, MapHandler
from llmui.core.agent.directed.lib.internal_state import Stage
from llmui.core.agent.directed.sections.common.models import ProjectInfo
from llmui.core.agent.directed.sections.debug.handlers.debug_handler import DebugHandler, DebugHandlerArgs
from llmui.core.agent.directed.sections.debug.states.debug_state import DebugStage
from llmui.core.agent.directed.sections.implementation.executors.list_files_executor import ListFilesExecutor
from llmui.core.agent.directed.sections.implementation.handlers.implementation_handler import ImplementationHandler, \
	ImplementationHandlerArgs
from llmui.core.agent.directed.sections.implementation.handlers.test_implementation_handler import \
	TestImplementationHandler, TestImplementationHandlerArgs
from llmui.core.agent.directed.sections.implementation.states.implementation_state import ImplementationStage
from llmui.core.agent.directed.sections.init.handlers.init_handler import InitHandler, InitHandlerArgs
from llmui.core.agent.directed.sections.init.states.init_state import InitStage
from llmui.core.agent.directed.sections.main.states.task_state import TaskState, TaskStage
from llmui.core.environment import LLMUIState, LLMUIAction
from llmui.di.handler_providers import HandlerProviders
from llmui.di.utils_providers import UtilsProviders


@dataclass
class TaskHandlerArgs:
	project_info: ProjectInfo
	debug: bool = True


class TaskHandler(MapHandler[TaskState, TaskHandlerArgs]):

	INTERNAL_STATE_CLS = TaskState

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__init_handler = InitHandler(self._llm)
		self.__implementation_handler = ImplementationHandler(self._llm)
		self.__test_implementation_handler = TestImplementationHandler(self._llm)
		self.__debug_handler = DebugHandler(self._llm)
		self.__analysis_db = UtilsProviders.provide_analysis_db()

	def _map_handlers(self) -> typing.Dict[Stage, Handler]:
		return {
			TaskStage.init: self.__init_handler,
			TaskStage.implementation: self.__implementation_handler,
			TaskStage.test_implementation: self.__test_implementation_handler,
			TaskStage.debug: self.__debug_handler
		}

	def _get_args(self, state: LLMUIState, args: TaskHandlerArgs) -> typing.Any:
		return {
			TaskStage.init: lambda: InitHandlerArgs(
				project_info=args.project_info
			),
			TaskStage.implementation: lambda: ImplementationHandlerArgs(
				project_info=self.__init_handler.internal_state.project_info
			),
			TaskStage.test_implementation: lambda: TestImplementationHandlerArgs(
				project_info=args.project_info,
				files=self.__implementation_handler.internal_state.implemented_files
			),
			TaskStage.debug: lambda: DebugHandlerArgs(
				project_info=args.project_info
			)
		}.get(self.stage)()

	def _next_stage(self, state: LLMUIState, args: TaskHandlerArgs) -> Stage:
		if self.__debug_handler.internal_state.stage == DebugStage.done:
			return TaskStage.done
		if self.__test_implementation_handler.internal_state.stage == ImplementationStage.done:
			return TaskStage.debug
		if self.__implementation_handler.internal_state.stage == ImplementationStage.done:
			if not args.debug:
				return TaskStage.done
			return TaskStage.test_implementation
		if self.__init_handler.internal_state.done:
			return TaskStage.implementation
		return TaskStage.init

	def _init_internal_state(self) -> TaskState:
		return TaskState(TaskStage.init)
