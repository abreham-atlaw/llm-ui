from llmui.core.agent.directed.lib.executor import LLMExecutor, I, O


class FormatExecutor(LLMExecutor[str, str]):

	def __init__(self, output_format, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__format = output_format

	def _prepare_prompt(self, arg: str) -> str:
		return f"""
\"\"\"{arg}\"\"\"
Can you format the above string to the following format:
{self.__format}
"""

	def _prepare_output(self, output: str, arg: str) -> str:
		return output
