import typing
from dataclasses import dataclass
from typing import Optional

from llmui.core.agent.directed.lib.handler import Handler
from llmui.core.agent.directed.sections.implementation.executors.dependencies_executor import DependenciesExecutor
from llmui.core.agent.directed.sections.implementation.states.dependencies_state import DependenciesState
from llmui.core.environment import LLMUIState, LLMUIAction
from llmui.utils.format_utils import FormatUtils


@dataclass
class DependenciesArgs:
	
	files_tasks: typing.Dict[str, str]
	descriptions: typing.Dict[str, str]
	ignored_files: typing.List[str]


class DependenciesHandler(Handler[DependenciesState, DependenciesArgs]):

	INTERNAL_STATE_CLS = DependenciesState

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__executor = DependenciesExecutor(self._llm)

	def _init_internal_state(self) -> DependenciesState:
		return DependenciesState()

	def __handle_dependency(
			self,
			file: str,
			files: typing.List[str],
			descriptions: typing.Dict[str, str],
			files_tasks: typing.Dict[str, str],
			project_description: str,
			task: str
	) -> typing.List[str]:
		dependencies = self.__executor.call((files, descriptions, files_tasks, file, project_description, task))
		if file in dependencies:
			dependencies.remove(file)
		return dependencies

	def _handle(self, state: LLMUIState, args: DependenciesArgs) -> Optional[LLMUIAction]:
		print("[+]Resolving Dependencies...")
		self.internal_state.dependencies = {}
		files = list(args.files_tasks.keys())
		for i, file in enumerate(files):
			print(f"[+]Processing file {file}...")
			self.internal_state.dependencies[file] = self.__handle_dependency(
				file,
				FormatUtils.filter_files(list(set(files + state.files)), args.ignored_files),
				args.descriptions,
				args.files_tasks,
				state.project_description,
				state.task
			)
			print(f"[+]Complete: {(i+1)*100/len(files) :.2f}%...", end="\r")
		return None
