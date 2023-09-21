import typing

from llmui.core.agent.directed_agent.handlers.formatters.formatter import Formatter
from llmui.core.environment import LLMUIState


class ImplementationPromptFormatter(Formatter):

	def __generate_dependencies_content(self, dependencies: typing.List[str], reader: typing.Callable) -> str:
		return "\n\n".join([
			f"""
//{file}
{reader(file)}
"""
			for file in dependencies
		])

	def format(self, file, description, dependencies: typing.List[str], project_description: str, reader: typing.Callable) -> str:
		return f"""
I would like it if you could help me on an app I was working on.

{project_description}

I have the following files:

{self.__generate_dependencies_content(dependencies, reader)}


I would like you to implement the file {file} which is responsible for {description}

"""
