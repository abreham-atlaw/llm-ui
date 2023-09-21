import typing

from dataclasses import dataclass
from typing import Optional

from llmui.core.agent.directed.lib.handler import Handler, A, S
from llmui.core.agent.directed.sections.implementation.executors.file_implementation_executor import \
	FileImplementationExecutor
from llmui.core.agent.directed.sections.implementation.states.files_implementation_state import FilesImplementationState
from llmui.core.environment import LLMUIState, LLMUIAction


@dataclass
class FilesImplementationArgs:
	files: typing.List[str]
	dependencies: typing.Dict[str, typing.List[str]]
	descriptions: typing.Dict[str, str]


class FilesImplementationHandler(Handler[FilesImplementationState, FilesImplementationArgs]):

	INTERNAL_STATE_CLS = FilesImplementationState

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__executor = FileImplementationExecutor(self._llm)

	def _init_internal_state(self) -> FilesImplementationState:
		return FilesImplementationState()

	@staticmethod
	def __order_files(files: typing.List[str], dependencies: typing.Dict[str, typing.List[str]]) -> typing.List[str]:
		return sorted(
			files,
			key=lambda file: len(dependencies[file])
		)

	def __implement_file(self, file: str, file_description: str, dependencies: typing.List[str], project_description: str, reader: typing.Callable) -> str:
		return self.__executor((
			project_description,
			file,
			file_description,
			{
				dependency: reader(dependency)
				for dependency in dependencies
			}
		))

	def handle(self, state: LLMUIState, args: FilesImplementationArgs) -> typing.Optional[LLMUIAction]:
		print("[+]Implementing Files ..")
		files = self.__order_files(
			files=args.files,
			dependencies=args.dependencies
		)

		for i, file in enumerate(files):
			if file in self.get_internal_state().implemented_files:
				continue
			print(f"[+]Complete: {i * 100 / len(args.files) :.2f}%... Implementing {file}")
			content = self.__implement_file(
				file,
				args.descriptions[file],
				args.dependencies[file],
				state.project_description,
				state.read_content
			)
			self.get_internal_state().implemented_files.append(file)
			return LLMUIAction(
				"write",
				[
					file,
					content
				]
			)
		self.get_internal_state().complete = True
		return None
