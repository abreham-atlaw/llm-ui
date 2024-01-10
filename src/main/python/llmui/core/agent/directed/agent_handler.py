import typing
from dataclasses import dataclass
from typing import Optional

from llmui.core.agent.directed.lib.handler import Handler, A, S, MapHandler
from llmui.core.agent.directed.lib.internal_state import Stage, StagedInternalState
from llmui.core.agent.directed.sections.init.handlers.init_handler import InitHandler
from llmui.core.environment import LLMUIState, LLMUIAction


@dataclass
class MainHandlerArgs:
	pass


class MainHandlerStage(Stage):
	init = 0
	implementation = 1
	debug = 2
	done = 3


@dataclass
class MainHandlerState(StagedInternalState):
	pass


class MainHandler(MapHandler[MainHandlerState, MainHandlerArgs]):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__init_handler = InitHandler

	def _map_handlers(self) -> typing.Dict[Stage, Handler]:
		return {

		}


	def _get_args(self, state: LLMUIState, args: A) -> typing.Any:
		pass

	def _next_stage(self, state: LLMUIState, args: A) -> Stage:
		pass

	INTERNAL_STATE_CLS = MainHandlerState

	def _init_internal_state(self) -> MainHandlerState:
		return MainHandlerState(MainHandlerStage.init)

	def _handle(self, state: LLMUIState, args: MainHandlerArgs) -> Optional[LLMUIAction]:

