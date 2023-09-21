import typing

import re
from enum import Enum

from llmui.core.agent.directed.lib.executor import LLMExecutor


class ListFilesExecutor(LLMExecutor[typing.Tuple[str, typing.List[str], typing.Dict[str, str], 'ListFilesExecutor.Mode'], typing.Dict[str, str]]):

	class Mode(Enum):
		implement = 0
		test = 1
		feature = 2

	def __get_mode_query(self, mode: 'ListFilesExecutor.Mode'):
		return {
			ListFilesExecutor.Mode.implement: "I wanted to implement the app. Can you make a numbered list of all new files(their paths) with their description(like the one below) I must implement?",
			ListFilesExecutor.Mode.test: "I wanted to test the app.  Can you make a numbered list of all new files(their paths) with their description(like the one below) I must implement to test the already functioning app?",
			ListFilesExecutor.Mode.feature: "I wanted to add the feature.",  # TODO
		}.get(mode)

	@staticmethod
	def __generate_file_descriptions(files_list: typing.List[str], descriptions: typing.Dict[str, str]) -> str:
		return "\n".join([
			f"{file}: {descriptions.get(file, '')}"
			for file in files_list
		])

	def __get_implemented_files(self, files: typing.List[str], descriptions: typing.Dict[str, str]) -> str:
		if len(files) == 0:
			return ""
		return f"""
Here are the list of files of implemented:
{self.__generate_file_descriptions(files, descriptions)}
"""

	def _prepare_prompt(self, arg: typing.Tuple[str, typing.List[str], typing.Dict[str, str], 'ListFilesExecutor.Mode']) -> str:
		project_description, files, descriptions, mode = arg
		return f"""
I would like it if you could help me on an app I was working on.
{project_description}
{self.__get_implemented_files(files, descriptions)}
{self.__get_mode_query(mode)}
1. lib/apps/auth/application/blocs/AuthBloc.dart: This file defines the AuthBloc class, which manages the authentication state of the app.
2. lib/apps/auth/application/events/AuthEvent.dart: This file defines the AuthEvent class, which represents the events that can be emitted by the AuthBloc.
Note: Only include files(not folders).
"""


	def _prepare_output(self, output: str, arg: str) -> typing.Dict[str, str]:
		text = output.replace("*", "").replace("`", "")
		pattern = r'\d+\. (\S+): (.+)'
		matches = re.findall(pattern, text)

		result = {}
		for match in matches:
			path, description = match
			result[path] = description

		return result
