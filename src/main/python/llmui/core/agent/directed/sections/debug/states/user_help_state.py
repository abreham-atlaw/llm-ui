import typing
from dataclasses import dataclass

from llmui.core.agent.directed.lib.internal_state import InternalState


@dataclass
class UserHelpState(InternalState):
	user_input: typing.Optional[str] = None
