import typing
from dataclasses import dataclass
from typing import Optional

from llmui.core.agent.directed.lib.handler import Handler, A, S
from llmui.core.agent.directed.sections.common.models import ProjectInfo
from llmui.core.agent.directed.sections.init.executors.list_commands_executor import ListCommandsExecutor
from llmui.core.agent.directed.sections.init.handlers.commands_handler import CommandsHandler, CommandsHandlerArgs
from llmui.core.agent.directed.sections.init.states.setup_state import SetupState
from llmui.core.environment import LLMUIState, LLMUIAction


@dataclass
class SetupHandlerArgs:
	project_info: ProjectInfo


class SetupHandler(Handler[SetupState, SetupHandlerArgs]):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__list_command_executor = ListCommandsExecutor(self._llm)
		self.__commands_handler = CommandsHandler(self._llm)

	def _init_internal_state(self) -> SetupState:
		return SetupState()

	def handle(self, state: LLMUIState, args: SetupHandlerArgs) -> Optional[LLMUIAction]:
		if self.internal_state.commands is None:
			self.internal_state.commands = self.__list_command_executor((
				args.project_info.description,
				args.project_info.tech_stack)
			)
			return None

		if self.__commands_handler.internal_state.done:
			self.internal_state.done = True
			return None

		return self.__commands_handler.handle(
			state,
			CommandsHandlerArgs(
				commands=self.internal_state.commands
			)
		)
