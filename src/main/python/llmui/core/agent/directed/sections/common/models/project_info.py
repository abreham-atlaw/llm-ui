import typing
from dataclasses import dataclass


@dataclass
class ProjectInfo:
	tech_stack: typing.List[str]
	task: str
	ignored_files: typing.List[str]
