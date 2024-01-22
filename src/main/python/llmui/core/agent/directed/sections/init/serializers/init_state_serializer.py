import typing

from llmui.core.agent.directed.lib.serializer import InternalStateSerializer
from llmui.core.agent.directed.sections.common.models import ProjectInfo
from llmui.core.agent.directed.sections.init.states.init_state import InitState


class InitStateSerializer(InternalStateSerializer):

	def __init__(self):
		super().__init__(InitState)

	def serialize(self, state: InitState) -> typing.Dict[str, typing.Any]:
		data = super().serialize(state)
		if state.project_info is not None:
			data["project_info"] = state.project_info.__dict__.copy()
		return data

	def deserialize(self, data: typing.Dict[str, typing.Any]) -> InitState:
		if data["project_info"] is not None:
			data["project_info"] = ProjectInfo(**data["project_info"])
		return super().deserialize(data)
