import typing
from dataclasses import dataclass

from llmui.core.agent.directed.sections.implementation.executors.list_files_executor import ListFilesExecutor
from llmui.core.agent.directed.sections.implementation.handlers.implementation_handler import ImplementationHandlerArgs, \
	ImplementationHandler
from llmui.core.agent.directed.sections.implementation.handlers.list_files_handler import ListFilesHandlerArgs
from llmui.core.environment import LLMUIState


@dataclass
class TestImplementationHandlerArgs(ImplementationHandlerArgs):
	files: typing.List[str]


class TestImplementationHandler(ImplementationHandler):

	def _get_list_files_args(self, state: LLMUIState, args: TestImplementationHandlerArgs) -> ListFilesHandlerArgs:
		arg = super()._get_list_files_args(state, args)
		arg.mode = ListFilesExecutor.Mode.test
		arg.files_to_test = args.files
		return arg
