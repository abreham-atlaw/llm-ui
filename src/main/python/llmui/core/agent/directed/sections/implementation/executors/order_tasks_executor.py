import typing

from llmui.core.agent.directed.lib.executor import LLMExecutor
from llmui.core.agent.directed.sections.common.executors.format_executor import FormatExecutor
from llmui.utils.format_utils import FormatUtils


class OrderTasksExecutor(LLMExecutor[typing.Dict[str, str], typing.List[str]]):

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
{file}
{task}
"""
			for file, task in files_tasks.items()
		])

	def _prepare_prompt(self, arg: typing.Dict[str, str]) -> str:
		files_tasks = arg
		return f"""
I have the following task for each file:

{self.__prepare_file_task(files_tasks)}

In what order should I modify/implement the files? Just list the file paths.
"""

	def _prepare_output(self, output: str, arg: typing.Dict[str, str]) -> typing.List[str]:
		output = self.__format_executor(output)
		tasks = FormatUtils.extract_list_from_json_string(output)
		return tasks