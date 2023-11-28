import typing
from dataclasses import dataclass

from llmui.core.agent.directed.lib.handler import MapHandler, Handler
from llmui.core.agent.directed.lib.internal_state import Stage
from llmui.core.agent.directed.sections.common.models import ProjectInfo
from llmui.core.agent.directed.sections.debug.handlers.check_results_handler import CheckResultsHandler
from llmui.core.agent.directed.sections.debug.handlers.check_stuck_status_handler import CheckStuckStatusHandler
from llmui.core.agent.directed.sections.debug.handlers.docker_prep_handler import DockerPrepHandler, \
	DockerPrepHandlerArgs
from llmui.core.agent.directed.sections.debug.handlers.error_extraction_handler import ErrorExtractionHandler
from llmui.core.agent.directed.sections.debug.handlers.list_files_handler import ListFilesHandler
from llmui.core.agent.directed.sections.debug.handlers.modify_handler import ModifyHandler, ModifyHandlerArgs
from llmui.core.agent.directed.sections.debug.handlers.run_handler import RunHandler
from llmui.core.agent.directed.sections.debug.handlers.user_help_handler import UserHelpHandler
from llmui.core.agent.directed.sections.debug.states.debug_state import DebugState, DebugStage
from llmui.core.environment import LLMUIState


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
		self.__modify_handler = ModifyHandler(self._llm)
		self.__check_results_handler = CheckResultsHandler(self._llm)
		self.__check_stuck_status_handler = CheckStuckStatusHandler(self._llm)
		self.__user_help_handler = UserHelpHandler(self._llm)

		self.__non_reset_handlers = [
			self.__prep_handler
		]

	def _map_handlers(self) -> typing.Dict[DebugStage, Handler]:
		return {
			DebugStage.prep: self.__prep_handler,
			DebugStage.error_extraction: self.__error_extractor_handler,
			DebugStage.list_files: self.__list_files_handler,
			DebugStage.modify: self.__modify_handler,
			DebugStage.run: self.__run_handler,
			DebugStage.check_results: self.__check_results_handler,
			DebugStage.check_stuck: self.__check_stuck_status_handler,
			DebugStage.user_help: self.__user_help_handler
		}

	def __get_error_message(self) -> str:
		if self.__check_stuck_status_handler.get_internal_state().is_stuck:
			return self.__user_help_handler.get_internal_state().user_input
		return self.__error_extractor_handler.get_internal_state().extracted_message

	def _get_args(self, state: LLMUIState, args: DebugHandlerArgs) -> typing.Any:
		arg_function = {
			DebugStage.prep: lambda: DockerPrepHandlerArgs(args.project_info.tech_stack),
			DebugStage.list_files: self.__get_error_message,
			DebugStage.modify: lambda: ModifyHandlerArgs(
				relevant_files=self.__list_files_handler.get_internal_state().files,
				error_message=self.__get_error_message()
			),
		}.get(self.get_internal_state().stage)
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
			DebugStage.run: DebugStage.check_results,
			DebugStage.error_extraction: DebugStage.list_files,
			DebugStage.user_help: DebugStage.list_files,
			DebugStage.list_files: DebugStage.modify,
		}.get(self.get_internal_state().stage)

		if next_stage is not None:
			return next_stage

		if self.get_internal_state().stage == DebugStage.check_results:
			if self.__check_results_handler.get_internal_state().passed:
				return DebugStage.done
			return DebugStage.check_stuck

		if self.get_internal_state().stage == DebugStage.check_stuck:
			if self.__check_stuck_status_handler.get_internal_state().is_stuck:
				return DebugStage.user_help
			return DebugStage.error_extraction

		if self.get_internal_state().stage == DebugStage.modify:
			if self.__modify_handler.get_internal_state().done:
				self.__prepare_for_cycle()
				return DebugStage.run
			return DebugStage.modify

		raise Exception("Next Stage not found")

	def _init_internal_state(self) -> DebugState:
		return DebugState()
