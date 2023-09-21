import typing

from lib.rl.agent import Agent
from llmui.core.agent.directed_agent.exceptions import HandlerNotFoundException
from llmui.core.agent.directed_agent.handlers.dependencies_handler import DependenciesHandler
from llmui.core.agent.directed_agent.handlers.handler import StageHandler, HandlerContext
from llmui.core.agent.directed_agent.handlers.implementation_handler import ImplementationHandler
from llmui.core.agent.directed_agent.handlers.init_handler import InitHandler
from llmui.core.agent.directed_agent.stage import Stage
from llmui.core.agent.directed_agent.state import InternalState
from llmui.core.environment import LLMUIAction, LLMUIState
from llmui.llm import LLM


class DirectedAgent(Agent[LLMUIState, LLMUIAction]):

	def __init__(self, llm: LLM):
		super().__init__()
		self.__llm = llm
		self.__llm.reset()
		self._state = InternalState(None, None, None, None)
		self.__handlers: typing.Dict[Stage, StageHandler] = {
			stage: handler_class(self.__llm)
			for stage, handler_class in {
				Stage.INIT: InitHandler,
				Stage.LISTED: DependenciesHandler,
				Stage.DEPENDENCY_LISTED: ImplementationHandler
			}.items()
		}

	@staticmethod
	def __identify_stage(state: LLMUIState, internal_state: InternalState) -> Stage:
		if internal_state.files is None:
			return Stage.INIT
		if internal_state.dependencies is None:
			return Stage.LISTED
		for file in internal_state.files:
			if file not in internal_state.implemented_files:
				return Stage.DEPENDENCY_LISTED
		return Stage.IMPLEMENTED

	def __handle_stage(self, stage: Stage, state: LLMUIState) -> typing.Optional[LLMUIAction]:
		handler = self.__handlers.get(stage)
		if handler is None:
			raise HandlerNotFoundException(stage)
		return handler.handle(
			stage,
			self._state,
			state,
			HandlerContext(
"""
App Name: Foodie Friends

Description: Foodie Friends is a social food delivery app that connects users with local restaurants and food vendors. Users can browse a wide range of culinary delights, read reviews from other users, and order food for delivery or pick-up. The app also features a community forum where users can share food recommendations, ask questions, and connect with other foodies.

Required Pages:

	Home page: This is the main page of the app where users can browse restaurants and food vendors. The page should also display popular dishes, recent orders, and upcoming events.
	Restaurant page: This page provides detailed information about a specific restaurant, such as its menu, hours of operation, and contact information. Users can also read reviews from other users and place an order for delivery or pick-up.
	Food page: This page provides detailed information about a specific dish, such as its ingredients, nutritional information, and reviews from other users.
	Cart page: This page allows users to view the items they have added to their cart and checkout.
	Profile page: This page allows users to create a profile, edit their account settings, and view their order history.
	Community forum: This page allows users to connect with other foodies, share food recommendations, and ask questions.

It'll use the flutter with the following folder structure.

lib
├── apps
│ ├── auth
│ │ ├── application
│ │ │ ├── blocs
│ │ │ ├── events
│ │ │ ├── forms
│ │ │ └── states
│ │ ├── data
│ │ │ ├── models
│ │ │ ├── repositories
│ │ │ └── requests
│ │ └── presentation
│ │ ├── screens
│ │ └── widgets
│ └── core
│ │ ├── application
│ │ │ ├── blocs
│ │ │ ├── events
│ │ │ ├── forms
│ │ │ └── states
│ │ ├── data
│ │ │ ├── models
│ │ │ ├── repositories
│ │ │ └── requests
│ │ └── presentation
│ │ │ ├── screens
│ │ │ └── widgets
├── configs
│ ├── content_configs.dart
│ ├── data_configs.dart
│ └── ui_configs.dart
├── main.dart
└── router.dart

"""
			)
		)

	def _policy(self, state: LLMUIState) -> typing.Optional[LLMUIAction]:
		stage = self.__identify_stage(state, self._state)
		return self.__handle_stage(stage, state)
