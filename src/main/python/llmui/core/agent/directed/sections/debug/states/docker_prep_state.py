from dataclasses import dataclass

from llmui.core.agent.directed.lib.internal_state import InternalState


@dataclass
class DockerPrepState(InternalState):
	complete: str = False
