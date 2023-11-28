import typing

from llmui.core.agent.directed.lib.executor import LLMExecutor, I, O
from llmui.utils.format_utils import FormatUtils


class CheckStuckStatusExecutor(LLMExecutor[typing.List[str], bool]):

	@staticmethod
	def __prepare_errors_list(errors: typing.List[str]) -> str:
		return ",\n".join([f"```rawtext\n{error}```" for error in errors])

	def _prepare_prompt(self, arg: typing.List[str]) -> str:
		return f"""
Are the following errors the same:
{self.__prepare_errors_list(arg)}
Format your answer in the following format:
{{
same: 0 // 0 if false 1 if true
}}
"""

	def _prepare_output(self, output: str, arg: typing.List[str]) -> bool:
		return bool(int(FormatUtils.extract_json_from_string(output).get("same")))
