import typing

from dataclasses import dataclass

from llmui.core.agent.directed.lib.internal_state import InternalState


@dataclass
class ListFilesState(InternalState):

	files: typing.Optional[typing.List[str]] = None
	descriptions: typing.Optional[typing.Dict[str, str]] = None
