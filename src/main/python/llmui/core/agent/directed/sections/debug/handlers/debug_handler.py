import typing
from dataclasses import dataclass

from llmui.core.agent.directed.lib.handler import MapHandler, Handler
from llmui.core.agent.directed.lib.internal_state import Stage
from llmui.core.agent.directed.sections.common.models import ProjectInfo
from llmui.core.agent.directed.sections.debug.handlers.cause_handler import CauseHandler, CauseHandlerArgs
from llmui.core.agent.directed.sections.debug.handlers.check_results_handler import CheckResultsHandler
from llmui.core.agent.directed.sections.debug.handlers.check_stuck_status_handler import CheckStuckStatusHandler
from llmui.core.agent.directed.sections.debug.handlers.docker_prep_handler import DockerPrepHandler, \
	DockerPrepHandlerArgs
from llmui.core.agent.directed.sections.debug.handlers.error_extraction_handler import ErrorExtractionHandler, \
	ErrorExtractionHandlerArgs
from llmui.core.agent.directed.sections.debug.handlers.modify_handler import ModifyHandler, ModifyHandlerArgs
from llmui.core.agent.directed.sections.debug.handlers.run_handler import RunHandler
from llmui.core.agent.directed.sections.debug.handlers.user_help_handler import UserHelpHandler, UserHelpHandlerArgs
from llmui.core.agent.directed.sections.debug.states.debug_state import DebugState, DebugStage
from llmui.core.agent.directed.sections.debug.states.error_extraction_state import Error
from llmui.core.agent.directed.sections.implementation.executors.list_files_executor import ListFilesExecutor
from llmui.core.agent.directed.sections.implementation.handlers.files_implementation_handler import \
	FilesImplementationHandler, FilesImplementationArgs
from llmui.core.agent.directed.sections.implementation.handlers.implementation_handler import ImplementationHandler, \
	ImplementationHandlerArgs
from llmui.core.agent.directed.sections.implementation.handlers.list_files_handler import ListFilesHandler, \
	ListFilesHandlerArgs
from llmui.core.agent.directed.sections.implementation.states.implementation_state import ImplementationStage
from llmui.core.environment import LLMUIState
from llmui.di.handler_providers import HandlerProviders


@dataclass
class DebugHandlerArgs:
	project_info: ProjectInfo


class DebugHandler(MapHandler[DebugState, DebugHandlerArgs]):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__prep_handler = DockerPrepHandler(self._llm)
		self.__error_extractor_handler = ErrorExtractionHandler(self._llm)
		self.__list_files_handler = ListFilesHandler(self._llm)
		self.__run_handler = RunHandler(self._llm)
		self.__implementation_handler = FilesImplementationHandler(self._llm)
		self.__check_results_handler = CheckResultsHandler(self._llm)
		self.__check_stuck_status_handler = CheckStuckStatusHandler(self._llm)
		self.__user_help_handler = UserHelpHandler(self._llm)
		self.__cause_handler = CauseHandler(self._llm)

		self.__analysis_handler = HandlerProviders.provide_analysis_handler()
		self.__non_reset_handlers = [
			self.__prep_handler
		]

	def _map_handlers(self) -> typing.Dict[DebugStage, Handler]:
		return {
			DebugStage.prep: self.__prep_handler,
			DebugStage.error_extraction: self.__error_extractor_handler,
			DebugStage.list_files: self.__list_files_handler,
			DebugStage.modify: self.__implementation_handler,
			DebugStage.run: self.__run_handler,
			DebugStage.check_results: self.__check_results_handler,
			DebugStage.check_stuck: self.__check_stuck_status_handler,
			DebugStage.cause_extraction: self.__cause_handler,
			DebugStage.user_help: self.__user_help_handler
		}

	def __choose_error(self, errors: typing.List[Error]) -> Error:
		return errors[0]

	def __get_solution(self) -> str:
		if self.__check_stuck_status_handler.internal_state.is_stuck:
			return self.__user_help_handler.internal_state.user_input
		return self.__cause_handler.internal_state.cause

	def _get_args(self, state: LLMUIState, args: DebugHandlerArgs) -> typing.Any:
		arg_function = {
			DebugStage.prep: lambda: DockerPrepHandlerArgs(args.project_info),
			DebugStage.list_files: lambda: ListFilesHandlerArgs(
				mode=ListFilesHandler.Mode.debug,
				project_info=ProjectInfo(
					task=self.__get_solution(),
					tech_stack=args.project_info.tech_stack,
					ignored_files=args.project_info.ignored_files,
					docs=args.project_info.docs
				)
			),
			DebugStage.cause_extraction: lambda: CauseHandlerArgs(
				error=self.__choose_error(self.__error_extractor_handler.internal_state.errors),
				project_info=args.project_info
			),
			DebugStage.modify: lambda: FilesImplementationArgs(
				files_tasks=self.__list_files_handler.internal_state.tasks,
				project_info=ProjectInfo(
					task=self.__get_solution(),
					tech_stack=args.project_info.tech_stack,
					ignored_files=args.project_info.ignored_files,
					docs=args.project_info.docs
				)
			),
			DebugStage.error_extraction: lambda: ErrorExtractionHandlerArgs(
				error=self.__run_handler.internal_state.output
			),
			DebugStage.user_help: lambda: UserHelpHandlerArgs(
				error=self.__run_handler.internal_state.output
			)
		}.get(self.internal_state.stage)
		if arg_function is None:
			return None
		return arg_function()

	def __prepare_for_cycle(self):
		for handler in self._get_all_handlers():
			if handler not in self.__non_reset_handlers:
				handler.reset()

	def _next_stage(self, state: LLMUIState, args: DebugHandlerArgs) -> Stage:
		next_stage = {
			DebugStage.prep: DebugStage.run,
			DebugStage.error_extraction: DebugStage.cause_extraction,
			DebugStage.user_help: DebugStage.list_files,
			DebugStage.list_files: DebugStage.modify,
		}.get(self.internal_state.stage)

		if next_stage is not None:
			return next_stage

		if self.internal_state.stage == DebugStage.check_results:
			if self.__check_results_handler.internal_state.passed:
				return DebugStage.done
			return DebugStage.check_stuck

		if self.internal_state.stage == DebugStage.check_stuck:
			if self.__check_stuck_status_handler.internal_state.is_stuck:
				return DebugStage.user_help
			return DebugStage.error_extraction

		if self.internal_state.stage == DebugStage.modify:
			if self.__implementation_handler.internal_state.complete:
				self.__prepare_for_cycle()
				return DebugStage.run
			return DebugStage.modify

		if self.internal_state.stage == DebugStage.run:
			if self.__run_handler.internal_state.done:
				return DebugStage.check_results
			return DebugStage.run

		if self.internal_state.stage == DebugStage.cause_extraction:
			if self.__cause_handler.internal_state.done:
				return DebugStage.list_files
			return DebugStage.cause_extraction

		raise Exception("Next Stage not found")

	def _init_internal_state(self) -> DebugState:
		return DebugState()
