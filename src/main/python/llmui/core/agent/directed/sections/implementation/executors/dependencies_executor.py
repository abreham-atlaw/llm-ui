import typing

import re

from llmui.core.agent.directed.lib.executor import LLMExecutor
from llmui.core.agent.directed.sections.common.executors.format_executor import FormatExecutor
from llmui.utils.format_utils import FormatUtils


class DependenciesExecutor(LLMExecutor[
							typing.Tuple[typing.List[str], typing.Dict[str, str],  typing.Dict[str, str], str, typing.List[str], str],
							typing.List
						]):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__format_executor = FormatExecutor(
			llm=self._llm,
			output_format="""
{
	"0": path/to/first/file,
	"1": path/to/second/file,
	"2": path/to/third/file
}
If there are no files leave '{}'
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
			f"{i+1}. {file}: {descriptions.get(file, 'Not Implemented yet.')}"
			for i, file in enumerate(files_list)
		])

	def _prepare_prompt(self, arg: typing.Tuple[typing.List[str], typing.Dict[str, str],  typing.Dict[str, str], str, typing.List[str], str]) -> str:
		files_list, descriptions, file_tasks, file, docs, task = arg
		return f"""
Consider the following documentation:
{FormatUtils.format_docs(docs)}

I wanted to accomplish the following task:
{task}

Given the following relevant files:
{self.__generate_file_descriptions(files_list, descriptions)}

On which files does the file and task below directly depend on?
{self.__generate_file_descriptions(list(file_tasks.keys()), file_tasks)}

Just simply list the files paths. Try minimizing the number of dependencies
"""

	def _prepare_output(self, output: str, arg: typing.Tuple[typing.List[str], typing.Dict[str, str],  typing.Dict[str, str], str, typing.List[str], str]) -> typing.List[str]:
		output = self.__format_executor(output)
		files = FormatUtils.extract_list_from_json_string(output)
		return files
