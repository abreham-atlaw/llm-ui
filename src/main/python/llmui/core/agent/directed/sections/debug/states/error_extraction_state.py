import typing
from dataclasses import dataclass

from llmui.core.agent.directed.lib.internal_state import InternalState


@dataclass
class ErrorExtractionState(InternalState):
	extracted_message: typing.Optional[str] = None
