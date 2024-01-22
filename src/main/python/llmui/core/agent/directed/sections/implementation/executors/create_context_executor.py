import typing

from llmui.core.agent.directed.lib.executor import LLMExecutor, I, O
from llmui.utils.format_utils import FormatUtils


class CreateContextExecutor(LLMExecutor[typing.Tuple[str, typing.List[str], str, str], str]):

	def _prepare_prompt(self, arg: typing.Tuple[str, typing.List[str], str, str]) -> str:
		description, docs, project_task, task = arg
		return f"""
Given the project description:
{description}

And given the following documentation:
{FormatUtils.format_docs(docs)}

And finally given this larger task:
{project_task}

Can you extract all the important information for the following task:
 - {task}
"""

	def _prepare_output(self, output: str, arg: typing.Tuple[str, typing.List[str], str, str]) -> str:
		return output
