import typing
from dataclasses import dataclass

from llmui.core.agent.directed.lib.handler import Handler, MapHandler
from llmui.core.agent.directed.lib.internal_state import Stage
from llmui.core.agent.directed.lib.serializer import InternalStateSerializer
from llmui.core.agent.directed.sections.common.models import ProjectInfo
from llmui.core.agent.directed.sections.init.handlers.analysis_handler import AnalysisHandler, \
	AnalysisHandlerArgs
from llmui.core.agent.directed.sections.init.handlers.fuse_task_handler import FuseTaskHandler, FuseTaskHandlerArgs
from llmui.core.agent.directed.sections.init.handlers.setup_handler import SetupHandler, SetupHandlerArgs
from llmui.core.agent.directed.sections.init.serializers.init_state_serializer import InitStateSerializer
from llmui.core.agent.directed.sections.init.states.init_state import InitState, InitStage
from llmui.core.environment import LLMUIState
from llmui.di.handler_providers import HandlerProviders


@dataclass
class InitHandlerArgs:
	project_info: ProjectInfo
	setup: bool = False


class InitHandler(MapHandler[InitState, InitHandlerArgs]):

	INTERNAL_STATE_CLS = InitState

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__setup_handler = SetupHandler(self._llm)
		self.__analyze_handler = HandlerProviders.provide_analysis_handler()
		self.__fuse_task_handler = FuseTaskHandler(self._llm)

	# def set_handlers(self, setup, fuse):
	# 	self.__setup_handler = setup
	# 	self.__fuse_task_handler = fuse

	def _map_handlers(self) -> typing.Dict[Stage, Handler]:
		return {
			InitStage.setup: self.__setup_handler,
			InitStage.analysis: self.__analyze_handler,
			InitStage.fuse: self.__fuse_task_handler
		}

	def _get_args(self, state: LLMUIState, args: InitHandlerArgs) -> typing.Any:
		return {
			InitStage.setup: lambda: SetupHandlerArgs(
				project_info=ProjectInfo(
					task=state.project_description,
					tech_stack=args.project_info.tech_stack,
					ignored_files=args.project_info.ignored_files
				)
			),
			InitStage.analysis: lambda: AnalysisHandlerArgs(
				args.project_info.ignored_files
			),
			InitStage.fuse: lambda: FuseTaskHandlerArgs(
				description=state.project_description,
				task=args.project_info.task
			)
		}.get(self.stage)()

	def _next_stage(self, state: LLMUIState, args: InitHandlerArgs) -> InitStage:

		if self.internal_state.stage == InitStage.analysis:
			return InitStage.fuse
		if self.__setup_handler.internal_state.done:
			return InitStage.analysis
		return InitStage.setup

	def _init_internal_state(self) -> InitState:
		return InitState(InitStage.setup)

	def _get_handler(self, internal_state: InitState, state: LLMUIState, args: InitHandlerArgs) -> Handler:
		if not args.setup and internal_state.stage == InitStage.setup:
			internal_state.stage = InitStage.analysis
		return super()._get_handler(internal_state, state, args)

	def _post_handle(self, state: LLMUIState, args: InitHandlerArgs):

		if self.stage == InitStage.fuse:
			self.internal_state.project_info = ProjectInfo(
				tech_stack=args.project_info.tech_stack,
				task=self.__fuse_task_handler.internal_state.fused_task,
				ignored_files=args.project_info.ignored_files
			)
			self.internal_state.done = True

	# def export_config(self) -> typing.Dict[str, typing.Any]:
	# 	config = super().export_config()
	# 	config = {
	# 		"self": config,
	# 		"setup": self.__setup_handler.export_config(),
	# 		"fuse": self.__fuse_task_handler.export_config()
	# 	}
	#
	# 	return config

	# @classmethod
	# def load_config(cls, config: typing.Dict[str, typing.Any], *args, **kwargs) -> 'Handler':
	# 	handler: InitHandler = super(InitHandler, cls).load_config(
	# 		config.get("self"),
	# 		*args,
	# 		**kwargs
	# 	)
	# 	handler.set_handlers(
	# 		setup=SetupHandler.load_config(config.get("setup"), *args, **kwargs),
	# 		fuse=FuseTaskHandler.load_config(
	# 			config.get("fuse"),
	# 			*args,
	# 			**kwargs
	# 		)
	# 	)
	# 	return handler

	@classmethod
	def _get_serializer(cls) -> InternalStateSerializer:
		return InitStateSerializer()

	def _get_child_handlers(self):
		return [
			handler
			for handler in super()._get_child_handlers()
			if not isinstance(handler, AnalysisHandler)
		]
