from llmui.core.agent.directed.lib.executor import LLMExecutor, I, O


class SummarizeTaskExecutor(LLMExecutor[str, str]):

	def _prepare_prompt(self, arg: str) -> str:
		return f"""
Can you make the text below shorter without removing any information that is required to complete all the tasks.
{arg}
"""

	def _prepare_output(self, output: str, arg: str) -> str:
		return output
