import typing
from dataclasses import dataclass

from llmui.core.agent.directed.lib.handler import MapHandler, Handler
from llmui.core.agent.directed.lib.internal_state import Stage
from llmui.core.agent.directed.sections.common.models import ProjectInfo
from llmui.core.agent.directed.sections.implementation.executors.list_files_executor import ListFilesExecutor
from llmui.core.agent.directed.sections.implementation.handlers.dependencies_handler import DependenciesHandler, \
	DependenciesArgs
from llmui.core.agent.directed.sections.implementation.handlers.files_implementation_handler import \
	FilesImplementationHandler, FilesImplementationArgs
from llmui.core.agent.directed.sections.implementation.handlers.list_files_handler import ListFilesHandler, \
	ListFilesHandlerArgs
from llmui.core.agent.directed.sections.implementation.states.implementation_state import ImplementationState, \
	ImplementationStage
from llmui.core.environment import LLMUIState


@dataclass
class ImplementationHandlerArgs:
	project_info: ProjectInfo


class ImplementationHandler(MapHandler[ImplementationState, ImplementationHandlerArgs]):
	INTERNAL_STATE_CLS = ImplementationState

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__list_files_handler = ListFilesHandler(self._llm)
		self.__files_implementation_handler = FilesImplementationHandler(self._llm)

	def _map_handlers(self) -> typing.Dict[ImplementationStage, Handler]:
		return {
			ImplementationStage.list_files: self.__list_files_handler,
			ImplementationStage.implement_files: self.__files_implementation_handler
		}

	def _get_list_files_args(self, state: LLMUIState, args: ImplementationHandlerArgs) -> ListFilesHandlerArgs:
		return ListFilesHandlerArgs(
			ListFilesHandler.Mode.implementation,
			args.project_info
		)

	def __get_implement_files_args(self, state: LLMUIState, args: ImplementationHandlerArgs) -> FilesImplementationArgs:
		return FilesImplementationArgs(
			self.__list_files_handler.internal_state.tasks,
			args.project_info
		)

	def _generate_project_task(self, project_info: ProjectInfo) -> str:
		return project_info.task

	def _get_args(self, state: LLMUIState, args: ImplementationHandlerArgs) -> typing.Any:
		if self.internal_state.project_task is None:
			self.internal_state.project_task = self._generate_project_task(args.project_info)
		args.project_info = ProjectInfo(
			tech_stack=args.project_info.tech_stack,
			task=self.internal_state.project_task,
			ignored_files=args.project_info.ignored_files,
			docs=args.project_info.docs
		)
		return {
			ImplementationStage.list_files: self._get_list_files_args,
			ImplementationStage.implement_files: self.__get_implement_files_args
		}.get(self.internal_state.stage)(state, args)

	def _next_stage(self, state: LLMUIState, args: ImplementationHandlerArgs) -> Stage:
		if self.__files_implementation_handler.internal_state.complete:
			return ImplementationStage.done
		if self.__list_files_handler.internal_state.tasks is not None:
			return ImplementationStage.implement_files
		return ImplementationStage.list_files

	def _init_internal_state(self) -> ImplementationState:
		return ImplementationState(stage=ImplementationStage.list_files)

	def _post_handle(self, state: LLMUIState, args: ImplementationHandlerArgs):
		if self.__files_implementation_handler.internal_state.complete:
			self.internal_state.implemented_files = self.__files_implementation_handler.internal_state.implemented_files
