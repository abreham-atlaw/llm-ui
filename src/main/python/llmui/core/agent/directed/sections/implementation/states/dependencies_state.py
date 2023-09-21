import typing

from llmui.core.agent.directed.lib.internal_state import InternalState


class DependenciesState(InternalState):

	dependencies: typing.Optional[typing.Dict[str, typing.List[str]]] = None
