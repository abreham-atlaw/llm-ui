import os.path
import typing
from dataclasses import dataclass

from llmui.core.agent.directed.lib.handler import Handler
from llmui.core.agent.directed.sections.common.models import ProjectInfo
from llmui.core.agent.directed.sections.implementation.executors.list_files_executor import ListFilesExecutor
from llmui.core.agent.directed.sections.implementation.states.list_files_state import ListFilesState
from llmui.core.environment import LLMUIState, LLMUIAction
from llmui.utils.format_utils import FormatUtils


@dataclass
class ListFilesHandlerArgs:
	mode: ListFilesExecutor.Mode
	files_descriptions: typing.Dict[str, str]
	project_info: ProjectInfo
	files_to_test: typing.Optional[typing.List[str]] = None


class ListFilesHandler(Handler[ListFilesState, ListFilesHandlerArgs]):

	INTERNAL_STATE_CLS = ListFilesState

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__executor = ListFilesExecutor(self._llm)

	def _init_internal_state(self) -> ListFilesState:
		return ListFilesState()

	def __filter_files(self, root_dir: str, tasks: typing.Dict[str, str]) -> typing.Dict[str, str]:
		return {
			file: task
			for file, task in tasks.items()
			if not os.path.isdir(os.path.join(root_dir, file))
		}

	def __get_files(
			self,
			project_info: ProjectInfo,
			files: typing.List[str],
			analysis: typing.Dict[str, str],
			mode: ListFilesExecutor.Mode,
			files_to_test: typing.List[str],
			root_path: str,
			reader: typing.Callable,
			final_call: bool = False
	):
		files = self.__executor((
			project_info.task,
			project_info.tech_stack,
			files,
			analysis,
			mode,
			files_to_test
		))
		files = self.__filter_files(root_path, files)
		if final_call:
			return files
		files = list(files.keys())
		analysis = {
			file: reader(file)
			for file in files
			if os.path.exists(os.path.join(root_path, file))
		}
		return self.__get_files(
			project_info,
			files,
			analysis,
			mode,
			files_to_test,
			root_path,
			reader,
			final_call=True
		)

	def _handle(self, state: LLMUIState, args: ListFilesHandlerArgs) -> typing.Optional[LLMUIAction]:
		print("[+]Listing Relevant Files...")
		self.internal_state.tasks = self.__get_files(
			project_info=args.project_info,
			files=FormatUtils.filter_files(state.files, args.project_info.ignored_files),
			analysis=args.files_descriptions,
			mode=args.mode,
			files_to_test=args.files_to_test,
			reader=state.read_content,
			root_path=state.root_path
		)
		return None
