import dataclasses
from dataclasses import dataclass, field

import typing

from llmui.core.agent.directed.lib.internal_state import InternalState


@dataclass
class Command:
	command: str
	args: typing.List[str]


@dataclass
class SetupState(InternalState):
	commands: typing.Optional[typing.List[Command]] = None
	done: bool = False
