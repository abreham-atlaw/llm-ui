from typing import Optional

from llmui.core.agent.directed.lib.handler import Handler, A, S
from llmui.core.agent.directed.sections.debug.executors.list_files_executor import ListFilesExecutor
from llmui.core.agent.directed.sections.debug.states.list_files_state import ListFilesState
from llmui.core.environment import LLMUIState, LLMUIAction


class ListFilesHandler(Handler[ListFilesState, str]):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__executor = ListFilesExecutor(self._llm)

	def _init_internal_state(self) -> ListFilesState:
		return ListFilesState()

	def _handle(self, state: LLMUIState, args: str) -> Optional[LLMUIAction]:
		print("[+]Listing Files...")
		self.internal_state.files = self.__executor.call((state.root_path, args, state.read_content))
		return None
