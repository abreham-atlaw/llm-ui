import typing

from dataclasses import dataclass

from llmui.config import IMPLEMENTATION_TRIES
from llmui.core.agent.directed.lib.handler import Handler
from llmui.core.agent.directed.sections.common.models import ProjectInfo
from llmui.core.agent.directed.sections.implementation.executors.apply_snippet_executor import ApplySnippetExecutor
from llmui.core.agent.directed.sections.implementation.executors.content_check_executor import ContentCheckExecutor
from llmui.core.agent.directed.sections.implementation.executors.dependencies_executor import DependenciesExecutor
from llmui.core.agent.directed.sections.implementation.executors.file_implementation_executor import \
	FileImplementationExecutor
from llmui.core.agent.directed.sections.implementation.executors.order_tasks_executor import OrderTasksExecutor
from llmui.core.agent.directed.sections.implementation.handlers.dependencies_handler import DependenciesHandler, \
	DependenciesArgs
from llmui.core.agent.directed.sections.implementation.states.files_implementation_state import FilesImplementationState
from llmui.core.agent.directed.sections.init.handlers.analysis_handler import AnalysisHandlerArgs
from llmui.core.environment import LLMUIState, LLMUIAction
from llmui.di.handler_providers import HandlerProviders


class InvalidImplementationException(Exception):
	pass


@dataclass
class FilesImplementationArgs:
	files_tasks: typing.Dict[str, str]
	project_info: ProjectInfo
	tries: int = IMPLEMENTATION_TRIES


class FilesImplementationHandler(Handler[FilesImplementationState, FilesImplementationArgs]):

	INTERNAL_STATE_CLS = FilesImplementationState

	def __init__(self, *args,  **kwargs):
		super().__init__(*args, **kwargs)
		self.__executor = FileImplementationExecutor(self._llm)
		self.__order_executor = OrderTasksExecutor(self._llm)
		self.__content_check_executor = ContentCheckExecutor(self._llm)
		self.__dependencies_handler = DependenciesHandler(self._llm)
		self.__analysis_handler = HandlerProviders.provide_analysis_handler()
		self.__apply_snippet_executor = ApplySnippetExecutor(self._llm)

	def _init_internal_state(self) -> FilesImplementationState:
		return FilesImplementationState()

	def __order_files(self, files_tasks: typing.Dict[str, str]) -> typing.List[str]:
		if len(files_tasks) == 1:
			return list(files_tasks.keys())
		print("[+]Ordering Files...")
		ordered_files = self.__order_executor(files_tasks)
		for file in files_tasks.keys():
			if file not in ordered_files:
				ordered_files.append(file)
		for file in ordered_files:
			if file not in files_tasks.keys():
				ordered_files.remove(file)
		return ordered_files

	def __resolve_dependencies(self, state: LLMUIState, file: str, task: str, analysis: typing.Dict[str, str], ignored_files: typing.List[str]) -> typing.List[str]:
		self.__dependencies_handler.handle(
			state,
			DependenciesArgs(
				files_tasks={
					file: task
				},
				descriptions=analysis,
				ignored_files=ignored_files
			)
		)
		return self.__dependencies_handler.internal_state.dependencies[file]

	def __is_valid_implementation(self, original_content: str, task: str, new_content: str) -> bool:
		print("[+]Verifying Implementation...")
		if new_content.strip() == "":
			return False
		if original_content.strip() == "":
			return True
		return self.__content_check_executor((original_content, task, new_content))

	def __complete_content(self, original_content: str, task: str, new_content: str, apply_snippet=True) -> str:
		if self.__is_valid_implementation(original_content, task, new_content):
			return new_content
		if not apply_snippet:
			raise InvalidImplementationException()
		print("[+]Applying Snippet")

		new_content = self.__apply_snippet_executor((original_content, new_content))
		return self.__complete_content(original_content, task, new_content, False)

	def __implement_file(
			self,
			file: str,
			file_task: str,
			project_task: str,
			tech_stack: typing.List[str],
			root_path: str,
			reader: typing.Callable,
			state: LLMUIState,
			analysis: typing.Dict[str, str],
			ignored_files: typing.List[str],
			tries: int,
	) -> str:

		dependencies = self.__resolve_dependencies(
			state=state,
			file=file,
			task=file_task,
			analysis=analysis,
			ignored_files=ignored_files
		)
		content = self.__executor((
			project_task,
			tech_stack,
			root_path,
			file,
			file_task,
			dependencies,
			reader
		))

		try:
			content = self.__complete_content(
				original_content=reader(file),
				task=file_task,
				new_content=content
			)
		except InvalidImplementationException as ex:
			if tries > 0:
				print("[-]InvalidImplementation. Reimplementing...")
				return self.__implement_file(file, file_task, project_task, tech_stack, root_path, reader, state, analysis, ignored_files, tries-1)
			raise ex

		return content

	def __analyze_project(self, state: LLMUIState, ignored_files: typing.List[str]):
		self.__analysis_handler.handle(
			state,
			AnalysisHandlerArgs(
				ignored_files=ignored_files
			)
		)

	def _handle(self, state: LLMUIState, args: FilesImplementationArgs) -> typing.Optional[LLMUIAction]:
		print("[+]Implementing Files...")

		if self.internal_state.implementation_order is None:
			self.internal_state.implementation_order = self.__order_files(args.files_tasks)
			return None
		files = self.internal_state.implementation_order

		for i, file in enumerate(files):
			if file in self.internal_state.implemented_files:
				continue
			print(f"[+]Complete: {i * 100 / len(files) :.2f}%...Implementing {file}")
			self.__analyze_project(state, args.project_info.ignored_files)
			content = self.__implement_file(
				file,
				args.files_tasks[file],
				project_task=args.project_info.task,
				tech_stack=args.project_info.tech_stack,
				reader=state.read_content,
				root_path=state.root_path,
				state=state,
				analysis=self.__analysis_handler.internal_state.analysis,
				ignored_files=args.project_info.ignored_files,
				tries=args.tries
			)
			self.internal_state.implemented_files.append(file)
			return LLMUIAction(
				"write",
				[
					file,
					content
				]
			)
		self.internal_state.complete = True
		return None
