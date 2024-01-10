import typing

from llmui.core.agent.directed_agent.handlers.handler import StageHandler, HandlerContext
from llmui.core.agent.directed_agent.handlers.formatters.list_files import \
	ListRequiredFilesGenerator
from llmui.core.agent.directed_agent.handlers.parsers.list_files import ListFilesParser
from llmui.core.agent.directed_agent.stage import Stage
from llmui.core.agent.directed_agent.state import InternalState
from llmui.core.environment import LLMUIState, LLMUIAction


class InitHandler(StageHandler):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__prompt_generator = ListRequiredFilesGenerator()
		self.__parser = ListFilesParser()

	def handle(
			self,
			stage: Stage,
			internal_state: InternalState,
			state: LLMUIState,
			context: HandlerContext
	) -> typing.Optional[LLMUIAction]:
		prompt = self.__prompt_generator.format(context.project_description)
		response = self._get_llm().chat(prompt)
		files = self.__parser.parse(response)
		internal_state.files = list(files.keys())
		internal_state.files_tasks = files
		return None





