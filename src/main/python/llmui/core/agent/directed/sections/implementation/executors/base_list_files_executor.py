import typing
from abc import ABC

from llmui.core.agent.directed.lib.executor import LLMExecutor, I, O
from llmui.core.agent.directed.sections.common.executors.format_executor import FormatExecutor
from llmui.utils.format_utils import FormatUtils


class BaseListFilesExecutor(LLMExecutor[I, typing.Dict[str, str]], typing.Generic[I], ABC):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__format_executor = FormatExecutor(
			output_format="""
{
"path/to/file": "descriptions or modifications for file...", //both keys and values are stings
"path/to/file1": "descriptions or modifications for file1"
} 

Make sure the whole key strings are valid file paths.
And remove files that don't need modifications, duplicate files and invalid paths.
Also remove directories(keys should be a file not a dir)
Don't leave details from the tasks.
Just leave {} if there are no files.
""",
			llm=self._llm
		)

	def _prepare_output(self, output: str, arg: I) -> typing.Dict[str, str]:
		output = self.__format_executor(output)
		files_map = FormatUtils.extract_json_from_string(output)
		return files_map

