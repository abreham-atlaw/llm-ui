import typing
from dataclasses import dataclass
from typing import Optional

from llmui.core.agent.directed.lib.handler import Handler
from llmui.core.agent.directed.sections.common.models import ProjectInfo
from llmui.core.agent.directed.sections.debug.executors.cause_executor import CauseExecutor
from llmui.core.agent.directed.sections.debug.executors.list_debug_relevant_files_executor import \
	ListDebugRelevantFilesExecutor
from llmui.core.agent.directed.sections.debug.states.cause_state import CauseState
from llmui.core.agent.directed.sections.debug.states.error_extraction_state import Error
from llmui.core.agent.directed.sections.init.handlers.analysis_handler import AnalysisHandler
from llmui.core.environment import LLMUIState, LLMUIAction
from llmui.di.utils_providers import UtilsProviders


@dataclass
class CauseHandlerArgs:
	error: Error
	project_info: ProjectInfo


class CauseHandler(Handler[CauseState, CauseHandlerArgs]):

	INTERNAL_STATE_CLS = CauseState

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__list_files_executor = ListDebugRelevantFilesExecutor(self._llm)
		self.__executor = CauseExecutor(self._llm)
		self.__analysis_db = UtilsProviders.provide_analysis_db()

	def _init_internal_state(self) -> CauseState:
		return CauseState()

	def __get_docs(self, error: Error, project_info: ProjectInfo) -> typing.List[str]:
		return UtilsProviders.provide_documentation(project_info.docs).search(
			error.error,
			num_results=2
		)

	def __get_cause_docs(self, error: Error, files: typing.List[str], project_info: ProjectInfo, reader: typing.Callable) -> typing.List[str]:
		context = f"""
{error.error}
{''.join([reader(file) for file in files])}
"""
		docs = UtilsProviders.provide_documentation(project_info.docs).search(
			context,
			num_results=2,
		)
		return docs

	def _handle(self, state: LLMUIState, args: CauseHandlerArgs) -> Optional[LLMUIAction]:
		print("[+]Extracting Cause...")
		if self.internal_state.relevant_files is None:
			print("[+]Listing Relevant Files...")
			self.internal_state.relevant_files = list(self.__list_files_executor((
				args.error,
				self.__get_docs(args.error, args.project_info),
				self.__analysis_db.get_analysis(args.error.error, num_files=20, file_type=AnalysisHandler.FileType.file),
				state.read_content
			)).keys())
			return None
		self.internal_state.cause = self.__executor((
			args.error,
			self.internal_state.relevant_files,
			self.__get_cause_docs(args.error, self.internal_state.relevant_files, args.project_info, state.read_content),
			state.read_content))
		self.internal_state.done = True

