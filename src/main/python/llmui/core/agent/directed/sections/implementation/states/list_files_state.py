import typing

from dataclasses import dataclass

from llmui.core.agent.directed.lib.internal_state import InternalState


@dataclass
class ListFilesState(InternalState):
	tasks: typing.Optional[typing.Dict[str, str]] = None
