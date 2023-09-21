import typing

import re

from llmui.core.agent.directed_agent.handlers.parsers.parser import ResponseParser


class ListFilesParser(ResponseParser[typing.Dict[str, str]]):

	def parse(self, text: str) -> typing.Dict[str, str]:
		text = text.replace("*", "").replace("`", "")
		pattern = r'\d+\. (\S+): (.+)'
		matches = re.findall(pattern, text)

		result = {}
		for match in matches:
			path, description = match
			result[path] = description

		return result
