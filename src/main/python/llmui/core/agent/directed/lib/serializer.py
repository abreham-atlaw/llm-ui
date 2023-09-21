import dataclasses
import typing

from llmui.core.agent.directed.lib.internal_state import InternalState


class InternalStateSerializer:

	def __init__(self, cls=None):
		if cls is None:
			cls = InternalState
		self.__cls = cls

	def serialize(self, state: InternalState) -> typing.Dict[str, typing.Any]:
		return state.__dict__

	def deserialize(self, data: typing.Dict[str, typing.Any]) -> InternalState:
		try:
			instance = self.__cls()
			instance.__dict__.update(data)
		except TypeError:
			instance = self.__cls(**data)
		return instance
