import typing
from dataclasses import dataclass
from typing import Optional

from llmui.core.agent.directed.lib.handler import Handler
from llmui.core.agent.directed.sections.implementation.executors.dependencies_executor import DependenciesExecutor
from llmui.core.agent.directed.sections.implementation.states.dependencies_state import DependenciesState
from llmui.core.environment import LLMUIState, LLMUIAction


@dataclass
class DependenciesArgs:
	
	files: typing.List[str]
	descriptions: typing.Dict[str, str]


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
			project_description: str
	) -> typing.List[str]:
		return self.__executor.call((files, descriptions, file, project_description))

	def handle(self, state: LLMUIState, args: DependenciesArgs) -> Optional[LLMUIAction]:
		print("[+]Resolving Dependencies...")
		self.get_internal_state().dependencies = {}
		for i, file in enumerate(args.files):
			self.get_internal_state().dependencies[file] = self.__handle_dependency(
				file,
				list(set(args.files + state.files)),
				args.descriptions,
				state.project_description
			)
			print(f"[+]Complete: {(i+1)*100/len(args.files) :.2f}%... Resolved {file}", end="\r")
		return None
