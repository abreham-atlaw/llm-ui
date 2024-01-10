from dataclasses import dataclass

import typing
from typing import Optional

from llmui.core.agent.directed.lib.handler import Handler, A, S
from llmui.core.agent.directed.sections.init.states.commands_state import CommandsState
from llmui.core.agent.directed.sections.init.states.setup_state import Command
from llmui.core.environment import LLMUIState, LLMUIAction


@dataclass
class CommandsHandlerArgs:
	commands: typing.List[Command]


class CommandsHandler(Handler[CommandsState, CommandsHandlerArgs]):
	def _init_internal_state(self) -> CommandsState:
		return CommandsState()

	def _handle(self, state: LLMUIState, args: CommandsHandlerArgs) -> Optional[LLMUIAction]:
		for command in args.commands:
			if command not in self.internal_state.executed_commands:
				action = LLMUIAction(
					command="bash",
					args=[command.command] + command.args
				)
				self.internal_state.executed_commands.append(command)
				return action
		self.internal_state.done = True
		return None
