import typing
from dataclasses import dataclass, field

from llmui.core.agent.directed.lib.internal_state import InternalState
from llmui.core.agent.directed.sections.init.states.setup_state import Command


@dataclass
class CommandsState(InternalState):
	executed_commands: typing.List[Command] = field(default_factory=lambda: [])
	done: bool = False
