import typing

from llmui.core.agent.directed.lib.executor import LLMExecutor
from llmui.utils.format_utils import FormatUtils


class TaskToTestingExecutor(LLMExecutor[typing.Tuple[str, typing.List[str]], str]):

	def _prepare_prompt(self, arg: typing.Tuple[str, typing.List[str]]) -> str:
		task, docs = arg
		return f"""
I had the following task:

{task}

Write a new task for testing the functionalities of the above task which is aligned to the following documentation:
{FormatUtils.format_docs(docs)}

Note: Make the task a sentence or two long.
"""

	def _prepare_output(self, output: str, arg: typing.Tuple[str, typing.List[str]]) -> str:
		return output
