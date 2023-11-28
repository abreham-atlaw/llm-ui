import typing

import re

from llmui.core.agent.directed.lib.executor import LLMExecutor
from llmui.core.agent.directed.sections.common.executors.format_executor import FormatExecutor
from llmui.core.agent.directed.sections.debug.executors.implement_executor import ImplementExecutor
from llmui.utils.format_utils import FormatUtils


class ModifyExecutor(LLMExecutor[typing.Tuple[str, str, typing.List[str], typing.Callable], typing.Dict[str, str]]):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__implement_executor = ImplementExecutor(self._llm)
		self.__format_executor = FormatExecutor(
			llm=self._llm,
			output_format="""
{
"filename": "FILENAME" // file involved
"description": \"\"\"DESCRIPTION\"\"\" //how to handle it
}
"""
		)

	@staticmethod
	def __generate_file_content(filepath: str, read: typing.Callable) -> str:
		return f"""
//{filepath}
``` {read(filepath)} ```
"""
	
	@staticmethod
	def __extract_changes_map(text) -> typing.Dict[str, str]:
		pattern = r'{\s+"filename": \"(.*?)\",\s+"description": \"\"\"(.*?)\"\"\"'
		matches = re.findall(pattern, text, re.DOTALL)

		changes = {}
		for match in matches:
			filename = match[0]
			description = match[1].strip()
			changes[filename] = description

		return changes

	def _prepare_prompt(self, arg: typing.Tuple[str, str, typing.List[str], typing.Callable]) -> str:
		path, error, files, read = arg
		return f"""
I have the following project:

{FormatUtils.tree(path)}

I tried running the tests but it failed with the error:
"{error}"

Here are the contents of the relevant files:
{
"".join([
	self.__generate_file_content(file, read)
	for file in files
])
}

Can you make a numbered list of the files that have to be altered to fix the issue? Format it as the following:

1. test.txt: NEW CODE

"""

	def _prepare_output(self, output: str, arg: typing.Tuple[str, str, typing.List[str], typing.Callable]) -> typing.Dict[str, str]:
		output = self.__format_executor(output)
		changes_map = self.__extract_changes_map(output)

		content_map = {}
		for file, changes in changes_map.items():
			content_map[file] = self.__implement_executor((file, changes, arg[-1]))
		return content_map
