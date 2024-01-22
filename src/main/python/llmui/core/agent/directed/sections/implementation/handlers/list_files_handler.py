import os.path
import typing
from dataclasses import dataclass

from llmui.core.agent.directed.lib.handler import Handler
from llmui.core.agent.directed.sections.common.models import ProjectInfo
from llmui.core.agent.directed.sections.implementation.executors.list_debug_files_executor import ListDebugFilesExecutor
from llmui.core.agent.directed.sections.implementation.executors.list_files_executor import ListFilesExecutor
from llmui.core.agent.directed.sections.implementation.executors.list_test_files_executor import ListTestFilesExecutor
from llmui.core.agent.directed.sections.implementation.executors.task_to_testing_executor import TaskToTestingExecutor
from llmui.core.agent.directed.sections.implementation.states.list_files_state import ListFilesState
from llmui.core.environment import LLMUIState, LLMUIAction
from llmui.di.utils_providers import UtilsProviders
from llmui.utils.format_utils import FormatUtils


@dataclass
class ListFilesHandlerArgs:
	mode: 'ListFilesHandler.Mode'
	project_info: ProjectInfo
	files_to_test: typing.Optional[typing.List[str]] = None


class ListFilesHandler(Handler[ListFilesState, ListFilesHandlerArgs]):

	class Mode:
		implementation = 0
		testing = 1
		debug = 2

	INTERNAL_STATE_CLS = ListFilesState

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__executor = ListFilesExecutor(self._llm)
		self.__debug_executor = ListDebugFilesExecutor(self._llm)
		self.__test_executor = ListTestFilesExecutor(self._llm)
		self.__analysis_db = UtilsProviders.provide_analysis_db()
		self.__task_to_testing_executor = TaskToTestingExecutor(self._llm)

	def _init_internal_state(self) -> ListFilesState:
		return ListFilesState()

	def __filter_files(self, root_dir: str, tasks: typing.Dict[str, str]) -> typing.Dict[str, str]:
		return {
			file: task
			for file, task in tasks.items()
			if not os.path.isdir(os.path.join(root_dir, file))
		}

	def __get_docs(self, mode: 'ListFilesHandler.Mode', project_info: ProjectInfo) -> typing.List[str]:

		documentation = UtilsProviders.provide_documentation(project_info.docs)
		if mode == ListFilesHandler.Mode.implementation:
			return documentation.search(project_info.task, num_results=2)
		if mode == ListFilesHandler.Mode.testing:
			return documentation.search(project_info.task, num_results=2)
		return documentation.search(project_info.task, num_results=2)

	def __get_files(
			self,
			project_info: ProjectInfo,
			files: typing.List[str],
			analysis: typing.Dict[str, str],
			mode: 'ListFilesHandler.Mode',
			files_to_test: typing.List[str],
			root_path: str,
			reader: typing.Callable,
			final_call: bool = False
	):
		if mode == ListFilesHandler.Mode.implementation:
			files = self.__executor((
				project_info.task,
				project_info.tech_stack,
				files,
				analysis,
				self.__get_docs(mode, project_info)
			))
		elif mode == ListFilesHandler.Mode.testing:
			files = self.__test_executor((
				self.__get_docs(mode, project_info),
				files_to_test,
				analysis,
				project_info.task
			))
		else:
			files = self.__debug_executor((
				project_info.task,
				project_info.tech_stack,
				files,
				analysis,
				self.__get_docs(mode, project_info)
			))
		files = self.__filter_files(root_path, files)
		return files
		# if final_call:
		#    return files
		# TODO: Find a better way to handler error correction. The current method sabotages the results of the first call.
		# files = list(files.keys())
		# analysis = {
		# 	file: reader(file)
		# 	for file in files
		# 	if os.path.exists(os.path.join(root_path, file))
		# }
		# return self.__get_files(
		# 	project_info,
		# 	files,
		# 	analysis,
		# 	mode,
		# 	files_to_test,
		# 	root_path,
		# 	reader,
		# 	final_call=True
		# )

	def _handle(self, state: LLMUIState, args: ListFilesHandlerArgs) -> typing.Optional[LLMUIAction]:
		print("[+]Listing Relevant Files...")
		self.internal_state.tasks = self.__get_files(
			project_info=args.project_info,
			files=FormatUtils.filter_files(state.files, args.project_info.ignored_files),
			analysis=self.__analysis_db.get_analysis(args.project_info.task),
			mode=args.mode,
			files_to_test=args.files_to_test,
			reader=state.read_content,
			root_path=state.root_path,
			final_call=True
		)
		return None
