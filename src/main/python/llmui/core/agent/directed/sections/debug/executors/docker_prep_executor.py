import re
import typing

from llmui.core.agent.directed.lib.executor import LLMExecutor
from llmui.utils.format_utils import FormatUtils


class DockerPrepExecutor(LLMExecutor[typing.Tuple[str, typing.List[str]], str]):

	@staticmethod
	def __extract_first_code_block(text) -> str:
		pattern = r"```(.+?)\n(.+?)```"
		match = re.search(pattern, text, re.DOTALL)
		if match:
			language = match.group(1)
			code = match.group(2)
			return code
		return ""

	def _prepare_prompt(self, arg: typing.Tuple[str, typing.List[str]]) -> str:
		root_path, tech_stack = arg
		return f"""
Assume I have the folder structure below:
{FormatUtils.tree(root_path)}

The project uses {', '.join(tech_stack)}.
Write a dockerfile that runs all the tests with fast fail ( if one of the tests fail it doesn't proceed to the next ). 
"""

	def _prepare_output(self, output: str, arg: str) -> str:
		return self.__extract_first_code_block(output)
