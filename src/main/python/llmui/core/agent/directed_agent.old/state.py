import typing

from dataclasses import dataclass


@dataclass
class InternalState:

	required_files: typing.Optional[typing.List[str]]
	descriptions: typing.Optional[typing.Dict[str, str]]
	implemented_files: typing.Optional[typing.List[str]]
	dependencies: typing.Optional[typing.Dict[str, typing.List[str]]]
