import typing
from dataclasses import dataclass

from llmui.core.agent.directed.lib.handler import MapHandler, Handler
from llmui.core.agent.directed.lib.internal_state import Stage
from llmui.core.agent.directed.sections.common.models import ProjectInfo
from llmui.core.agent.directed.sections.implementation.executors.list_files_executor import ListFilesExecutor
from llmui.core.agent.directed.sections.implementation.handlers.dependencies_handler import DependenciesHandler, \
	DependenciesArgs
from llmui.core.agent.directed.sections.implementation.handlers.files_implementation_handler import \
	FilesImplementationHandler, FilesImplementationArgs
from llmui.core.agent.directed.sections.implementation.handlers.list_files_handler import ListFilesHandler, \
	ListFilesHandlerArgs
from llmui.core.agent.directed.sections.implementation.states.implementation_state import ImplementationState, \
	ImplementationStage
from llmui.core.environment import LLMUIState


@dataclass
class ImplementationHandlerArgs:
	descriptions: typing.Dict[str, str]
	project_info: ProjectInfo


class ImplementationHandler(MapHandler[ImplementationState, ImplementationHandlerArgs]):
	INTERNAL_STATE_CLS = ImplementationState

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__list_files_handler = ListFilesHandler(self._llm)
		self.__files_implementation_handler = FilesImplementationHandler(self._llm)

	def _map_handlers(self) -> typing.Dict[ImplementationStage, Handler]:
		return {
			ImplementationStage.list_files: self.__list_files_handler,
			ImplementationStage.implement_files: self.__files_implementation_handler
		}

	# def set_handlers(
	# 		self,
	# 		list_files_handler=None,
	# 		files_implementation_handler=None
	# ):
	# 	if list_files_handler is not None:
	# 		self.__list_files_handler = list_files_handler
	# 	if files_implementation_handler is not None:
	# 		self.__files_implementation_handler = files_implementation_handler

	def _get_list_files_args(self, state: LLMUIState, args: ImplementationHandlerArgs) -> ListFilesHandlerArgs:
		return ListFilesHandlerArgs(
			ListFilesExecutor.Mode.implement,
			args.descriptions,
			args.project_info
		)

	def __get_implement_files_args(self, state: LLMUIState, args: ImplementationHandlerArgs) -> FilesImplementationArgs:
		return FilesImplementationArgs(
			self.__list_files_handler.internal_state.tasks,
			args.project_info
		)

	def _get_args(self, state: LLMUIState, args: ImplementationHandlerArgs) -> typing.Any:
		return {
			ImplementationStage.list_files: self._get_list_files_args,
			ImplementationStage.implement_files: self.__get_implement_files_args
		}.get(self.internal_state.stage)(state, args)

	def _next_stage(self, state: LLMUIState, args: ImplementationHandlerArgs) -> Stage:
		if self.__files_implementation_handler.internal_state.complete:
			return ImplementationStage.done
		if self.__list_files_handler.internal_state.tasks is not None:
			return ImplementationStage.implement_files
		return ImplementationStage.list_files

	def _init_internal_state(self) -> ImplementationState:
		return ImplementationState(stage=ImplementationStage.list_files)

	def _post_handle(self, state: LLMUIState, args: ImplementationHandlerArgs):
		if self.__files_implementation_handler.internal_state.complete:
			self.internal_state.implemented_files = self.__files_implementation_handler.internal_state.implemented_files

	# def export_config(self) -> typing.Dict[str, typing.Any]:
	# 	config = super().export_config()
	# 	config = {
	# 		"self": config,
	# 		"list_files_handler": self.__list_files_handler.export_config(),
	# 		"files_implementation_handler": self.__files_implementation_handler.export_config()
	# 	}
	# 	return config

	# @classmethod
	# def load_config(cls, config: typing.Dict[str, typing.Any], *args, **kwargs) -> 'Handler':
	# 	handler: ImplementationHandler = super(ImplementationHandler, cls).load_config(
	# 		config.get("self"),
	# 		*args,
	# 		**kwargs
	# 	)
	# 	handler.set_handlers(
	# 		list_files_handler=ListFilesHandler.load_config(config.get("list_files_handler"), *args, **kwargs),
	# 		files_implementation_handler=FilesImplementationHandler.load_config(
	# 			config.get("files_implementation_handler"),
	# 			*args,
	# 			**kwargs
	# 		)
	# 	)
	# 	return handler
