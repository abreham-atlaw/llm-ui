import typing

from llmui.core.agent.directed_agent.handlers.formatters.implementation import ImplementationPromptFormatter
from llmui.core.agent.directed_agent.handlers.handler import StageHandler, HandlerContext
from llmui.core.agent.directed_agent.handlers.parsers.implementation import ImplementationResponseParser
from llmui.core.agent.directed_agent.stage import Stage
from llmui.core.agent.directed_agent.state import InternalState
from llmui.core.environment import LLMUIState, LLMUIAction


class ImplementationHandler(StageHandler):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__prompt_formatter = ImplementationPromptFormatter()
		self.__response_parser = ImplementationResponseParser()

	@staticmethod
	def __order_files(files: typing.List[str], dependencies: typing.Dict[str, typing.List[str]]) -> typing.List[str]:
		return sorted(
			files,
			key=lambda file: len(dependencies[file])
		)

	def __implement_file(self, file: str, internal_state: InternalState, state: LLMUIState, context: HandlerContext) -> str:
		prompt = self.__prompt_formatter.format(
			file=file,
			description=internal_state.descriptions.get(file),
			dependencies=internal_state.dependencies.get(file),
			project_description=context.project_description,
			reader=state.read_content
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
		files = self.__order_files(
			files=internal_state.files,
			dependencies=internal_state.dependencies
		)

		for i, file in enumerate(files):
			if file in internal_state.implemented_files:
				continue
			content = self.__implement_file(file, internal_state, state, context)
			if internal_state.implemented_files is None:
				internal_state.implemented_files = []
			internal_state.implemented_files.append(file)
			return LLMUIAction(
				"write",
				[
					file,
					content
				]
			)
		return None
