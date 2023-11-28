import typing

import re

from llmui.core.agent.directed.lib.executor import LLMExecutor


class FileImplementationExecutor(LLMExecutor[typing.Tuple[str, typing.List[str], str, str, typing.Dict[str, str]], str]):

	@staticmethod
	def __extract_first_code_block(text) -> str:
		pattern = r"```(.+?)\n(.+?)```"
		match = re.search(pattern, text, re.DOTALL)
		if match:
			language = match.group(1)
			code = match.group(2)
			return code
		return ""

	@staticmethod
	def __generate_dependencies_content(dependencies: typing.Dict[str, str]) -> str:
		return "\n\n".join([
			f"""
//{file}
{content}
"""
			for file, content in dependencies.items()
		])

	def _prepare_prompt(self, arg: typing.Tuple[str, typing.List[str], str, str, typing.Dict[str, str]]) -> str:
		project_description, tech_stack, file, description, dependencies = arg
		return f"""
I would like it if you could help me on an app I was working on.

{project_description}

The project uses {', '.join(tech_stack)}

I have the following files:

{self.__generate_dependencies_content(dependencies)}


I would like you to implement the file {file} which is responsible for {description}
"""

	def _prepare_output(self, output: str, arg: typing.Tuple[str, typing.List[str], str, str, typing.Dict[str, str]]) -> str:
		return self.__extract_first_code_block(output)
