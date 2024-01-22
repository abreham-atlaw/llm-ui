import os.path
import typing
from dataclasses import dataclass
from typing import Optional

from llmui.core.agent.directed.lib.handler import Handler
from llmui.core.agent.directed.sections.implementation.executors.dependencies_executor import DependenciesExecutor
from llmui.core.agent.directed.sections.implementation.states.dependencies_state import DependenciesState
from llmui.core.agent.directed.sections.init.handlers.analysis_handler import AnalysisHandler
from llmui.core.environment import LLMUIState, LLMUIAction
from llmui.di.utils_providers import UtilsProviders


@dataclass
class DependenciesArgs:
	
	files_tasks: typing.Dict[str, str]
	docs: str


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
			files_tasks: typing.Dict[str, str],
			task: str,
			docs: str,
			root_dir: str
	) -> typing.List[str]:
		analysis = UtilsProviders.provide_analysis_db().get_analysis(
			files_tasks.get(file),
			num_files=8,
			file_type=AnalysisHandler.FileType.file
		)
		analysis.update(UtilsProviders.provide_analysis_db().get_analysis(
			files_tasks.get(file),
			num_files=2,
			file_type=AnalysisHandler.FileType.dir
		))
		analysis.update(
			UtilsProviders.provide_analysis_db().get_analysis(
				task,
				num_files=5
			)
		)
		files = list(analysis.keys())
		documentation = UtilsProviders.provide_documentation(docs)
		dependencies = self.__executor((
			files,
			analysis,
			files_tasks,
			file,
			(
				documentation.search(files_tasks.get(file), num_results=1) +
				documentation.search(task, num_results=1)
			),
			task
		))
		if file in dependencies:
			dependencies.remove(file)

		for dependency in dependencies:
			if os.path.isdir(os.path.join(root_dir, dependency)) or (dependency not in files and dependency not in files_tasks.keys()):
				dependencies.remove(dependency)

		return dependencies

	def _handle(self, state: LLMUIState, args: DependenciesArgs) -> Optional[LLMUIAction]:
		print("[+]Resolving Dependencies...")
		self.internal_state.dependencies = {}
		files = list(args.files_tasks.keys())
		for i, file in enumerate(files):
			print(f"[+]Processing file {file}...")
			self.internal_state.dependencies[file] = self.__handle_dependency(
				file,
				args.files_tasks,
				state.task,
				docs=args.docs,
				root_dir=state.root_path
			)
			print(f"[+]Complete: {(i+1)*100/len(files) :.2f}%...", end="\r")
		return None
