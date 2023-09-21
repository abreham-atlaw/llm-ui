import typing

import re

from llmui.core.agent.directed_agent.handlers.formatters.formatter import Formatter, LLMFormatter


class DependenciesPromptFormatter(Formatter):

	@staticmethod
	def __generate_file_descriptions(files_list: typing.List[str], descriptions: typing.Dict[str, str]) -> str:
		return "\n".join([
			f"{file}: {descriptions.get(file)}"
			for file in files_list
		])

	def format(self, files_list: typing.List[str], descriptions: typing.Dict[str, str], file: str, project_description: str) -> str:
		return f"""
I would like it if you could help me on an app I was working on.

{project_description}

Here are the list of file to be implemented:
{self.__generate_file_descriptions(files_list, descriptions)}

On Which files does the file {file}({descriptions.get(file)}) depend on?
"""
