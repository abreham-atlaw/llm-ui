import typing
from enum import IntEnum
from dataclasses import dataclass


class Stage(IntEnum):
	pass


@dataclass
class InternalState:
	pass


@dataclass
class StagedInternalState(InternalState):
	stage: Stage
