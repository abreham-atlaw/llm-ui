import typing

from enum import Enum

from llmui.core.agent.directed.lib.executor import LLMExecutor
from llmui.core.agent.directed.sections.common.executors.format_executor import FormatExecutor
from llmui.utils.format_utils import FormatUtils


class ListFilesExecutor(LLMExecutor[typing.Tuple[str, typing.List[str], typing.List[str], typing.Dict[str, str], 'ListFilesExecutor.Mode', typing.List[str]], typing.Dict[str, str]]):

	class Mode(Enum):
		implement = 0
		test = 1
		debug = 2

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__format_executor = FormatExecutor(
			output_format="""
{
"path/to/file": "task on file...",
"path/to/file1": "task for file1"
}

Make sure the whole key strings are valid file paths. And remove files that don't need modifications, duplicate files and invalid paths. Also remove directories(keys should be a file not a dir) 
""",
			llm=self._llm
		)

	def __get_mode_query(self, mode: 'ListFilesExecutor.Mode', task: str, files=None):
		if files is None:
			files = []
		return {
			ListFilesExecutor.Mode.test: f"""
I had the task:
{task}

I implemented the files:
{self.__generate_files_list(files)}

What files do I need to implement to test the files I just implemented. The new files will be containing unit tests, integration tests(if necessary) and so on. 
""",
			ListFilesExecutor.Mode.implement: f"""
I wanted to accomplish the following task.
{task}

Can you make a list of files(their paths, feel free to create new files) with what I need to do on the file?
Make it as detailed as possible.(include classes, functions to be implemented).
Only include files relevant to the task
""",
			ListFilesExecutor.Mode.debug: f"""
I tried running the test but it failed with the error below:
{task}

Can you make a list of files(their paths, feel free to create new files) with what I need to do on the file to fix the issue above?
Make it as detailed as possible(include classes, functions to be implemented).
"""
		}.get(mode).strip()

	@staticmethod
	def __generate_files_list(files_list: typing.List[str]) -> str:
		return "\n".join([
			f"{i+1}. {file}"
			for i, file in enumerate(files_list)
		])

	@staticmethod
	def __generate_file_descriptions(files_list: typing.List[str], descriptions: typing.Dict[str, str]) -> str:
		return "\n\n".join([
			f"{i+1}. {file}: {descriptions.get(file, '')}"
			for i, file in enumerate(files_list)
		])

	def __get_implemented_files(self, files: typing.List[str], descriptions: typing.Dict[str, str]) -> str:
		if len(files) == 0:
			return ""
		return f"""
Here are the list of files currently on the project:
{self.__generate_file_descriptions(files, descriptions)}
"""

	def _prepare_prompt(self, arg: typing.Tuple[str, typing.List[str], typing.List[str], typing.Dict[str, str], 'ListFilesExecutor.Mode', typing.List[str]]) -> str:
		task, tech_stack, files, descriptions, mode, files_to_test = arg
		return f"""
I would like it if you could help me on a project I was working on. Could you list the files(code, ignore assets) I have to work on?
The project uses {', '.join(tech_stack)}.

{self.__get_mode_query(mode, task, files=files_to_test)}

{self.__get_implemented_files(files, descriptions)}
Note: Only include files(not folders) & Only list files(code) that need to be modified or created to achieve the given task ignoring assets.
Minimize the number of files to modify or create.
You should also include only editable files not images, audio, ...
"""

	def _prepare_output(self, output: str, arg:  typing.Tuple[str, typing.List[str], typing.List[str], typing.Dict[str, str], 'ListFilesExecutor.Mode', typing.List[str]]) -> typing.Dict[str, str]:
		output = self.__format_executor(output)

		files_map = FormatUtils.extract_json_from_string(output)

		return files_map
