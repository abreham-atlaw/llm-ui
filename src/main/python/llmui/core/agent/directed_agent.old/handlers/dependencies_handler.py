import typing

from llmui.core.agent.directed_agent.handlers.formatters.dependencies import DependenciesPromptFormatter
from llmui.core.agent.directed_agent.handlers.handler import StageHandler, HandlerContext
from llmui.core.agent.directed_agent.handlers.parsers.dependencies import DependenciesResponseParser
from llmui.core.agent.directed_agent.stage import Stage
from llmui.core.agent.directed_agent.state import InternalState
from llmui.core.environment import LLMUIState, LLMUIAction


class DependenciesHandler(StageHandler):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__prompt_formatter = DependenciesPromptFormatter()
		self.__response_parser = DependenciesResponseParser(self._get_llm())

	def __handle_dependency(
			self,
			file: str,
			internal_state: InternalState,
			context: HandlerContext
	) -> typing.List[str]:
		prompt = self.__prompt_formatter.format(
			files_list=internal_state.files,
			descriptions=internal_state.descriptions,
			file=file,
			project_description=context.project_description
		)
		response = self._get_llm().chat(prompt)
		return self.__response_parser.parse(response)

	def handle(
			self,
			stage: Stage,
			internal_state: InternalState,
			state: LLMUIState,
			context: HandlerContext
	) -> typing.Optional[LLMUIAction]:
		dependencies = {}
		for file in internal_state.files:
			dependencies[file] = self.__handle_dependency(
				file, internal_state, context
			)
		internal_state.dependencies = dependencies
		return None
