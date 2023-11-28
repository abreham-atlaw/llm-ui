import typing
from dataclasses import dataclass


@dataclass
class ProjectInfo:
	tech_stack: typing.List[str]
	description: str
