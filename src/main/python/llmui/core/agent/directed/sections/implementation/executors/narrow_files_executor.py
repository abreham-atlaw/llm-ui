from llmui.core.agent.directed.lib.executor import LLMExecutor, I, O


class NarrowFilesExecutor(LLMExecutor):

	def _prepare_prompt(self, arg: I) -> str:

		return f"""

"""

	def _prepare_output(self, output: str, arg: I) -> O:
		pass