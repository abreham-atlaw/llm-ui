import typing

from llmui.core.agent.directed.lib.executor import LLMExecutor
from llmui.core.agent.directed.sections.common.executors.format_executor import FormatExecutor
from llmui.utils.format_utils import FormatUtils


class OrderTasksExecutor(LLMExecutor[typing.Tuple[typing.Dict[str, str], typing.List[str]], typing.List[str]]):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__format_executor = FormatExecutor(
			output_format="""
{
"0": "path/to/first/file",
"1": "path/to/second/file"
...
}
""",
			llm=self._llm
		)

	def __prepare_file_task(self, files_tasks: typing.Dict[str, str]) -> str:
		return "\n".join([
			f"""
{i+1}. {file}
{task}
"""
			for i, (file, task) in enumerate(files_tasks.items())
		])

	def _prepare_prompt(self, arg: typing.Tuple[typing.Dict[str, str], typing.List[str]]) -> str:
		files_tasks, docs = arg
		return f"""
Given the documentation below:

{FormatUtils.format_docs(docs)}

In what order should I implement/modify the files below. I've included the tasks for each file:

{self.__prepare_file_task(files_tasks)}

Just list the file paths.
"""

	def _prepare_output(self, output: str, arg: typing.Tuple[typing.Dict[str, str], typing.List[str]]) -> typing.List[str]:
		output = self.__format_executor(output)
		tasks = FormatUtils.extract_list_from_json_string(output)
		return tasks