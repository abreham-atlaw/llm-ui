import typing
from dataclasses import dataclass

from llmui.core.agent.directed.lib.internal_state import InternalState


@dataclass
class AnalyzeProjectState(InternalState):
	analysis: typing.Dict[str, str]
	analysis_sig: typing.Dict[str, str]
	types: typing.Dict[str, int]
