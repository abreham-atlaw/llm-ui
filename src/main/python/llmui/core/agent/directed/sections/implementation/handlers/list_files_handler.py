import os
import typing
from dataclasses import dataclass

from llmui.core.agent.directed.lib.executor import LLMExecutor
from llmui.core.agent.directed.lib.handler import Handler
from llmui.core.agent.directed.lib.internal_state import InternalState
from llmui.core.agent.directed.sections.implementation.executors.list_files_executor import ListFilesExecutor
from llmui.core.agent.directed.sections.implementation.states.list_files_state import ListFilesState
from llmui.core.environment import LLMUIState, LLMUIAction


@dataclass
class ListFilesHandlerArgs:
	mode: ListFilesExecutor.Mode
	files_descriptions: typing.Dict[str, str]


class ListFilesHandler(Handler[ListFilesState, ListFilesHandlerArgs]):

	INTERNAL_STATE_CLS = ListFilesState

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__executor = ListFilesExecutor(self._llm)

	def _init_internal_state(self) -> ListFilesState:
		return ListFilesState()

	def handle(self, state: LLMUIState, args: ListFilesHandlerArgs) -> typing.Optional[LLMUIAction]:

		files = self.__executor((state.project_description, state.files, args.files_descriptions, args.mode))
		self.get_internal_state().files = list(files.keys())
		self.get_internal_state().descriptions = files
		return None
