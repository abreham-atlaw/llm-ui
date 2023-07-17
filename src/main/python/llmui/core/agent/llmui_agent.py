import typing

import json
from json import JSONDecodeError

from lib.rl.agent import Agent
from lib.rl.agent.agent import S
from llmui.core.environment import LLMUIAction, LLMUIState
from llmui.llm import LLM


class LLMUIAgent(Agent[LLMUIState, LLMUIAction]):

	def __init__(self, llm: LLM):
		super().__init__()
		self.__llm = llm
		self.__llm.reset()
		self.__first_command = True

	def _prepare_query(self, state: LLMUIState) -> str:
		if self.__first_command:
			return f"""
{self._render_task()}
{self._render_manual()}

Note: The project might already contain files.
Enter you command in the form of json.
"""
		return f"""
{self._render_output(state.output)}
		
Enter you command in the form of json.
		"""

	def _render_task(self) -> str:
		return """
I would like you to develop a Python program that can serve as a user interface for Large Language Models and enable 
them to interact with the operating system. The program will assist the Large Language Model in constructing a 
substantial codebase. Specifically, the Large Language Model should be capable of reading files, writing files,
executing files, and viewing the results. The program should have a continuous loop that prompts the Large Language 
Model for input, executes the input, displays the output, and then prompts the Large Language Model for the next command
until the codebase is complete.
""".replace("\n", " ")

	def _render_manual(self) -> str:
		return """

Commands are represented as json of format:
{
"command": [command],
"args": [arg1, arg2,...]
}
Available commands and their args are:
write (write content into a file. Replaces content of the file if it already exists): 
-arg1: filepath,
-arg2: content
read (read content of a file):
-arg1: filepath
run (executes given linux command):
-arg1: linux_command
"""

	def _render_output(self, output: str) -> str:
		return f"""
Last Command Output:
{output}
"""

	def __prepare_response(self, response: str) -> LLMUIAction:
		json_ = json.loads(response)
		return LLMUIAction(json_["command"], json_["args"])

	def _policy(self, state: LLMUIState) -> LLMUIAction:
		query = self._prepare_query(state)
		response = self.__llm.chat(query)
		self.__first_command = False
		while True:
			try:
				return self.__prepare_response(response)
			except JSONDecodeError:
				response = self.__llm.chat("Please enter a valid json")
