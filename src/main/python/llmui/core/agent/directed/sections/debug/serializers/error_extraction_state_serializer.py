import typing

from lib.network import Serializer
from llmui.core.agent.directed.lib.internal_state import InternalState
from llmui.core.agent.directed.lib.serializer import InternalStateSerializer
from llmui.core.agent.directed.sections.debug.states.error_extraction_state import ErrorExtractionState, Error


class ErrorSerializer(Serializer):

	def __init__(self):
		super().__init__(Error)

	def serialize(self, data: Error) -> typing.Dict:
		return data.__dict__.copy()

	def deserialize(self, json_: typing.Dict) -> object:
		return Error(**json_)


class ErrorExtractionStateSerializer(InternalStateSerializer):

	def __init__(self):
		super().__init__(ErrorExtractionState)
		self.__error_serializer = ErrorSerializer()

	def serialize(self, state: ErrorExtractionState) -> typing.Dict[str, typing.Any]:
		data = super().serialize(state)
		if state.errors is not None:
			data["errors"] = [
				self.__error_serializer.serialize(error)
				for error in state.errors
			]
		return data

	def deserialize(self, data: typing.Dict[str, typing.Any]) -> InternalState:
		if data["errors"] is not None:
			data["errors"] = [
				self.__error_serializer.deserialize(error)
				for error in data["errors"]
			]
		return super().deserialize(data)
