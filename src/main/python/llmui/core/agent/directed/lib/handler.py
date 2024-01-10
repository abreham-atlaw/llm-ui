import json
import typing

from llmui.core.agent.directed.lib.internal_state import InternalState, StagedInternalState, Stage
from llmui.core.agent.directed.lib.serializer import InternalStateSerializer
from llmui.core.environment import LLMUIState, LLMUIAction
from llmui.llm import LLM

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional


S = TypeVar('S', bound=InternalState)
A = TypeVar('A')


class Handler(Generic[S, A], ABC):

	INTERNAL_STATE_CLS = InternalState

	def __init__(self, llm: LLM, auto_save_path: typing.Optional[str] = None):
		self._llm = llm
		self.__internal_state = self._init_internal_state()
		self.__auto_save_path = auto_save_path

	@abstractmethod
	def _init_internal_state(self) -> S:
		pass

	@property
	def internal_state(self) -> S:
		return self.get_internal_state()

	def get_internal_state(self) -> S:
		return self.__internal_state

	def _set_internal_state(self, internal_state: S):
		self.__internal_state = internal_state

	@abstractmethod
	def _handle(self, state: LLMUIState, args: A) -> Optional[LLMUIAction]:
		pass

	def handle(self, state: LLMUIState, args: A) -> Optional[LLMUIAction]:
		action = self._handle(state, args)
		if self.__auto_save_path is not None:
			self._auto_save()
		return action

	@classmethod
	def _get_serializer(cls) -> InternalStateSerializer:
		return InternalStateSerializer(cls=cls.INTERNAL_STATE_CLS)

	def export_config(self) -> typing.Dict[str, typing.Any]:
		serializer = self._get_serializer()
		return serializer.serialize(
			self.internal_state
		)

	def _auto_save(self):
		self.save(self.__auto_save_path)

	def save(self, path: str):
		config = self.export_config()
		with open(path, "w") as file:
			json.dump(config, file)

	def reset(self):
		print(f"[+]Resetting {self.__class__}...")
		self.__internal_state = self._init_internal_state()

	@classmethod
	def load_config(cls, config: typing.Dict[str, typing.Any], *args, **kwargs) -> 'Handler':
		handler = cls(*args, **kwargs)
		serializer = cls._get_serializer()
		handler._set_internal_state(
			serializer.deserialize(config)
		)
		return handler

	@classmethod
	def load_handler(cls, path, *args, **kwargs) -> 'Handler':
		with open(path) as file:
			config = json.load(file)
		return cls.load_config(config, *args, **kwargs)


MS = TypeVar('MS', bound=StagedInternalState)


class MapHandler(Handler[MS, A], ABC):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__handlers_map: typing.Optional[typing.Dict[Stage, Handler]] = None

	@property
	def stage(self) -> Stage:
		return self.internal_state.stage

	@stage.setter
	def stage(self, value: Stage):
		self.internal_state.stage = value

	@abstractmethod
	def _map_handlers(self) -> typing.Dict[Stage, Handler]:
		pass

	@abstractmethod
	def _get_args(self, state: LLMUIState, args: A) -> typing.Any:
		pass

	@abstractmethod
	def _next_stage(self, state: LLMUIState, args: A) -> Stage:
		pass

	def _get_handler_args(self, internal_state: S, state: LLMUIState, args: A) -> [Handler, A]:
		return self._get_handler(internal_state, state, args), self._get_args(state, args)

	def _get_handler(self, internal_state: S, state: LLMUIState, args: A) -> Handler:
		if self.__handlers_map is None:
			self.__handlers_map = self._map_handlers()
		return self.__handlers_map.get(internal_state.stage)

	def _get_all_handlers(self) -> typing.List[Handler]:
		return list(self.__handlers_map.values())

	def _post_handle(self, state: LLMUIState, args: A):
		pass

	def _handle(self, state: LLMUIState, args: A) -> typing.Optional[LLMUIAction]:
		handler, child_args = self._get_handler_args(self.internal_state, state, args)
		action = handler.handle(state, child_args)
		self._post_handle(state, args)
		self.stage = self._next_stage(state, args)
		return action

	def reset(self):
		super().reset()
		for handler in self._get_child_handlers():
			handler.reset()

	def _get_child_handlers(self):
		return list(self._map_handlers().values())

	def export_config(self) -> typing.Dict[str, typing.Any]:
		config = {
			"self": super().export_config(),
		}
		config.update({
			self.get_handler_name(handler): handler.export_config()
			for handler in self._get_child_handlers()
		})
		return config

	def __get_variable_name(self, value):
		for name, attribute in self.__dict__.items():
			if value is attribute:
				return name
		raise ValueError(f"Couldn't find name for value={value}")

	def set_handlers(self, **kwargs):

		for name, handler in kwargs.items():
			for current_handler in self._get_child_handlers():
				handler_name = self.get_handler_name(current_handler)
				variable_name = self.__get_variable_name(current_handler)
				if handler_name == name:
					self.__dict__[variable_name] = handler

	@classmethod
	def get_handler_name(cls, handler):
		return handler.__class__.__name__

	@classmethod
	def load_config(cls, config: typing.Dict[str, typing.Any], *args, **kwargs) -> 'Handler':

		def get_class(handler, class_name):
			for name, value in handler.__dict__.items():
				if cls.get_handler_name(value) == class_name:
					return value.__class__
			raise Exception(f"Class not found: {class_name}")

		handler: MapHandler = super(MapHandler, cls).load_config(
			config.pop("self"),
			*args,
			**kwargs
		)

		child_handlers = {
			name: get_class(handler, name).load_config(handler_config, *args, **kwargs)
			for name, handler_config in config.items()
		}

		handler.set_handlers(
			**child_handlers
		)
		return handler
