import typing

import re

from llmui.core.agent.directed.lib.executor import LLMExecutor
from llmui.core.agent.directed.sections.common.executors.format_executor import FormatExecutor
from llmui.utils.format_utils import FormatUtils


class DependenciesExecutor(LLMExecutor[
							typing.Tuple[typing.List[str], typing.Dict[str, str],  typing.Dict[str, str], str, str, str],
							typing.List
						]):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__format_executor = FormatExecutor(
			llm=self._llm,
			output_format="""
{
	"0": path/to/first/dependency,
	"1": path/to/second/dependency,
	"2": path/to/third/dependency
}
"""
		)

	@staticmethod
	def __extract_paths(string):
		pattern = r'\[([^]]+)\]'
		match = re.search(pattern, string)
		if match:
			paths = match.group(1).split(',')
			return [path.strip().replace("\"", "").replace("'", "") for path in paths]

	@staticmethod
	def __generate_file_descriptions(files_list: typing.List[str], descriptions: typing.Dict[str, str]) -> str:
		return "\n".join([
			f"{i}. {file}: {descriptions.get(file, 'Not Implemented yet.')}"
			for i, file in enumerate(files_list)
		])

	def _prepare_prompt(self, arg: typing.Tuple[typing.List[str], typing.Dict[str, str],  typing.Dict[str, str], str, str, str]) -> str:
		files_list, descriptions, file_tasks, file, project_description, task = arg
		return f"""
I would like it if you could help me on an app I was working on.

I wanted to accomplish the following tasks:
{task}

Here are the list of files in the project currently:
{self.__generate_file_descriptions(files_list, descriptions)}

{'And here is the task for the file I would modify:' if len(file_tasks) == 1 else 'And here are the tasks for each file I would modify:'}
{self.__generate_file_descriptions(list(file_tasks.keys()), file_tasks)}

Which of these files does one programmer need to read before modifying the file {file} to accomplish it's task? Feel free to includes files from the tasks list. Just simply list the files pathes.
Note: Can you limit the number of dependencies to a maximum of 5 files or less.
"""

	def _prepare_output(self, output: str, arg: typing.Tuple[typing.List[str], typing.Dict[str, str],  typing.Dict[str, str], str, str, str]) -> typing.List[str]:
		output = self.__format_executor(output)
		files = FormatUtils.extract_list_from_json_string(output)
		return files
