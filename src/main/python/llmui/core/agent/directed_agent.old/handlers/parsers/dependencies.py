import typing

import re

from llmui.core.agent.directed_agent.handlers.parsers.parser import ResponseParser, LLMResponseParser, T


class DependenciesResponseParser(LLMResponseParser[typing.List[str]]):

	@staticmethod
	def __extract_paths(string):
		pattern = r'\[([^]]+)\]'
		match = re.search(pattern, string)
		if match:
			paths = match.group(1).split(',')
			return [path.strip().replace("\"", "").replace("'", "") for path in paths]

	def parse(self, text: str) -> typing.List[str]:

		prompt = f"""
I wanted to get the files a module depends on and got the following response.

{text}

Can you list the dependencies in the following way:

[
file_path0,
file_path1
]

Note: Leave [] if there are no dependencies
"""
		response = self._llm.chat(prompt)
		return self.__extract_paths(response)
