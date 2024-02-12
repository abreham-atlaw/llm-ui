import typing
from dataclasses import dataclass

from llmui.core.agent.directed.lib.internal_state import InternalState


@dataclass
class Error:
	test_case: str
	file_path: str
	error: str


@dataclass
class ErrorExtractionState(InternalState):
	errors: typing.Optional[typing.List[Error]] = None
