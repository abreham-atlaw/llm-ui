import typing
from dataclasses import dataclass

from llmui.core.agent.directed.sections.common.models import ProjectInfo
from llmui.core.agent.directed.sections.implementation.executors.task_to_testing_executor import TaskToTestingExecutor
from llmui.core.agent.directed.sections.implementation.handlers.implementation_handler import ImplementationHandlerArgs, \
	ImplementationHandler
from llmui.core.agent.directed.sections.implementation.handlers.list_files_handler import ListFilesHandlerArgs, \
	ListFilesHandler
from llmui.core.environment import LLMUIState
from llmui.di.utils_providers import UtilsProviders


@dataclass
class TestImplementationHandlerArgs(ImplementationHandlerArgs):
	files: typing.List[str]


class TestImplementationHandler(ImplementationHandler):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__task_to_testing_executor = TaskToTestingExecutor(self._llm)

	def _generate_project_task(self, project_info: ProjectInfo) -> str:
		return self.__task_to_testing_executor((
				project_info.task,
				UtilsProviders.provide_documentation(project_info.docs).search("testing", num_results=1)
			))

	def _get_list_files_args(self, state: LLMUIState, args: TestImplementationHandlerArgs) -> ListFilesHandlerArgs:
		arg = super()._get_list_files_args(state, args)
		arg.mode = ListFilesHandler.Mode.testing
		arg.files_to_test = args.files
		return arg

