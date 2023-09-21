import typing

from llmui.core.agent.directed.lib.executor import LLMExecutor, I, O


class ErrorExtractionExecutor(LLMExecutor[str, str]):

	def _prepare_prompt(self, arg: str) -> str:
		return f"""
Can you extract a main error and stacktrace of the error below.
{arg}
"""

	def _prepare_output(self, output: str, arg: I) -> O:
		return output
