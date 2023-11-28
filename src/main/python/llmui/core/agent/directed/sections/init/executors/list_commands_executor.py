import json
import re
import typing

from llmui.core.agent.directed.lib.executor import LLMExecutor, I, O
from llmui.core.agent.directed.sections.common.executors.format_executor import FormatExecutor
from llmui.core.agent.directed.sections.init.states.setup_state import Command
from llmui.utils.format_utils import FormatUtils


class ListCommandsExecutor(LLMExecutor[
								typing.Tuple[
									str,
									typing.List[str]
								],
								typing.List[Command]
						]):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__format_executor = FormatExecutor(
			llm=self._llm,
			output_format="""
//Write the appropriate bash command in a way that it exectutes f"{command} {' '.join(args)}" 
{"value":[
	{
		"command": "bash_command",
		"args": [
			//ARG 1,
			//ARG 2
			]
	},
	{
		"command": "another_bash_command",
		"args": [
			//ARG 1,
			//ARG 2
			]
	},
	...
]}
"""
		)

	@staticmethod
	def __extract_commands(input_string: str) -> typing.List[Command]:
		data = FormatUtils.extract_json_from_string(input_string)
		data = data["value"]
		commands = [Command(item['command'], item['args']) for item in data]

		return commands

	def _prepare_prompt(self, arg: typing.Tuple[str, str]) -> str:
		project_description, tech_stack = arg
		return f"""
I have the following project:
{project_description}

I was using the following stack:
{tech_stack}

Can you list the bash commands I need to execute to setup my project? Make sure the commands are not interactive and one liners. 
"""

	def _prepare_output(self, output: str, arg: typing.Tuple[str, str]) -> typing.List[Command]:
		output = self.__format_executor(output)
		return self.__extract_commands(output)
