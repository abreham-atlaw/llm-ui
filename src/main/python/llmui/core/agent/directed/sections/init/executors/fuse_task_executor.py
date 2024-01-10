import typing

from llmui.core.agent.directed.lib.executor import LLMExecutor, I, O


class FuseTaskExecutor(LLMExecutor[
							typing.Tuple[str, str],
							str
	]):

	def _prepare_prompt(self, arg: typing.Tuple[str, str]) -> str:
		description, task = arg
		return f"""
I have the following description for a project:
{description}

I have the task below:
{task}

Can you rewrite the task with all the relevant information from the project description?
Make sure to include all the necessary details since this will be passed as a task for the engineer. 
"""

	def _prepare_output(self, output: str, arg: typing.Tuple[str, str]) -> str:
		return output
