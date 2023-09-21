import typing

import re

from llmui.core.agent.directed.lib.executor import LLMExecutor


class DependenciesExecutor(LLMExecutor[
							typing.Tuple[
								typing.List[str],
								typing.Dict[str, str],
								str,
								str
							],
							typing.List
						]):

	@staticmethod
	def __extract_paths(string):
		pattern = r'\[([^]]+)\]'
		match = re.search(pattern, string)
		if match:
			paths = match.group(1).split(',')
			return [path.strip().replace("\"", "").replace("'", "") for path in paths]

	@staticmethod
	def __generate_file_descriptions(files_list: typing.List[str], descriptions: typing.Dict[str, str]) -> str:
		return "\n".join([
			f"{file}: {descriptions.get(file)}"
			for file in files_list
		])

	def _prepare_prompt(self, arg: typing.Tuple[typing.List[str], typing.Dict[str, str], str, str]) -> str:
		files_list, descriptions, file, project_description = arg
		return f"""
I would like it if you could help me on an app I was working on.

{project_description}

Here are the list of file to be implemented:
{self.__generate_file_descriptions(files_list, descriptions)}

On Which files does the file {file}({descriptions.get(file)}) depend on?
"""

	def _prepare_output(self, output: str, arg: typing.Tuple[typing.List[str], typing.Dict[str, str], str, str]) -> typing.List[str]:
		prompt = f"""
I wanted to get the files a module depends on and got the following response.

{output}

Can you list the dependencies in the following way:

[
file_path0,
file_path1
]

Note: Leave [] if there are no dependencies
		"""
		response = self._llm.chat(prompt)
		return self.__extract_paths(response)
