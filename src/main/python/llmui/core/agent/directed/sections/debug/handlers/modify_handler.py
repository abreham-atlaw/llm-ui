import typing
from dataclasses import dataclass
from typing import Optional

from llmui.core.agent.directed.lib.handler import Handler, A, S
from llmui.core.agent.directed.sections.debug.executors.modify_executor import ModifyExecutor
from llmui.core.agent.directed.sections.debug.states.modify_state import ModifyState
from llmui.core.environment import LLMUIState, LLMUIAction


@dataclass
class ModifyHandlerArgs:
	relevant_files: typing.List[str]
	error_message: str


class ModifyHandler(Handler[ModifyState, ModifyHandlerArgs]):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__executor = ModifyExecutor(self._llm)

	def _init_internal_state(self) -> ModifyState:
		return ModifyState()

	def __is_done(self) -> bool:
		return set(self.get_internal_state().contents.keys()) == set(self.get_internal_state().implemented_files)

	def __is_prepared(self) -> bool:
		return self.get_internal_state().contents is not None

	def handle(self, state: LLMUIState, args: ModifyHandlerArgs) -> Optional[LLMUIAction]:

		if not self.__is_prepared():
			self.get_internal_state().contents = self.__executor.call((state.root_path, args.error_message, args.relevant_files, state.read_content))

		for file, content in self.get_internal_state().contents.items():
			if file in self.get_internal_state().implemented_files:
				continue
			self.get_internal_state().implemented_files.append(file)
			return LLMUIAction(
				"write",
				[
					file,
					content
				]
			)
		self.get_internal_state().done = True
		return None
