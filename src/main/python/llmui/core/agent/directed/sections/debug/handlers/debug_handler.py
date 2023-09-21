import typing

from llmui.core.agent.directed.lib.handler import MapHandler, Handler
from llmui.core.agent.directed.lib.internal_state import Stage
from llmui.core.agent.directed.sections.debug.handlers.docker_prep_handler import DockerPrepHandler
from llmui.core.agent.directed.sections.debug.handlers.error_extraction_handler import ErrorExtractionHandler
from llmui.core.agent.directed.sections.debug.handlers.list_files_handler import ListFilesHandler
from llmui.core.agent.directed.sections.debug.handlers.modify_handler import ModifyHandler, ModifyHandlerArgs
from llmui.core.agent.directed.sections.debug.handlers.run_handler import RunHandler
from llmui.core.agent.directed.sections.debug.states.debug_state import DebugState, DebugStage
from llmui.core.environment import LLMUIState


class DebugHandler(MapHandler[DebugState, None]):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__prep_handler = DockerPrepHandler(self._llm)
		self.__error_extractor_handler = ErrorExtractionHandler(self._llm)
		self.__list_files_handler = ListFilesHandler(self._llm)
		self.__run_handler = RunHandler(self._llm)
		self.__modify_handler = ModifyHandler(self._llm)

	def _map_handlers(self) -> typing.Dict[DebugStage, Handler]:
		return {
			DebugStage.prep: self.__prep_handler,
			DebugStage.error_extraction: self.__error_extractor_handler,
			DebugStage.list_files: self.__list_files_handler,
			DebugStage.modify: self.__modify_handler,
			DebugStage.run: self.__run_handler
		}

	def _get_args(self, state: LLMUIState, args: None) -> typing.Any:
		return {
			DebugStage.prep: lambda: None,
			DebugStage.error_extraction: lambda: None,
			DebugStage.list_files: lambda: self.__error_extractor_handler.get_internal_state().extracted_message,
			DebugStage.run: lambda: None,
			DebugStage.modify: lambda: ModifyHandlerArgs(
				relevant_files=self.__list_files_handler.get_internal_state().files,
				error_message=self.__error_extractor_handler.get_internal_state().extracted_message
			)
		}.get(self.get_internal_state().stage)()

	def _next_stage(self, state: LLMUIState, args: None) -> Stage:
		if self.__modify_handler.get_internal_state().done:
			return DebugStage.prep
		if len(self.__list_files_handler.get_internal_state().files) > 0:
			return DebugStage.modify
		if self.get_internal_state().stage == DebugStage.list_files:
			return DebugStage.modify
		if self.get_internal_state().stage == DebugStage.error_extraction:
			return DebugStage.list_files
		if self.get_internal_state().stage == DebugStage.run:
			return DebugStage.error_extraction
		if self.__prep_handler.get_internal_state().complete:
			return DebugStage.run
		return DebugStage.prep

	def _init_internal_state(self) -> DebugState:
		return DebugState()
