import typing

from lib.rl.agent import Agent
from lib.rl.agent.agent import S
from llmui.core.environment import LLMUIAction, LLMUIState
from llmui.llm import LLM


class LLMUIAgent(Agent[LLMUIState, LLMUIAction]):

	def __init__(self, llm: LLM):
		super().__init__()
		self.__llm = llm

	def _prepare_query(self, state: LLMUIState) -> str:
		return f"""
		{self._render_task()}
		{self._render_output(state.output)}
		{self._render_manual()}
		
		Fill in the blank:
		The command you want to execute is _______________.
		"""

	def _render_task(self) -> str:
		return """
		
		Assume you are a software engineer. Your task is to build a python TicTacToe game on CLI
		
		"""

	def _render_manual(self) -> str:
		return """
		
		Available Commands:
		
		write [file] [content] - Writes content to file
		read [file] - Reads content of file
		run [command] - Runs given linux command, [command]
		 
		"""

	def _render_output(self, output: str) -> str:
		return f"""
		
		Last Command Output:

		{output}
		
		"""

	def __prepare_response(self, response: str) -> LLMUIAction:
		return LLMUIAction(response)

	def _policy(self, state: LLMUIState) -> LLMUIAction:
		query = self._prepare_query(state)
		response = self.__llm.chat(query)
		return self.__prepare_response(response)
