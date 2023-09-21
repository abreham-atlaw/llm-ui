import re

from llmui.core.agent.directed_agent.handlers.parsers.parser import ResponseParser, LLMResponseParser, T


class ImplementationResponseParser(ResponseParser):

	@staticmethod
	def __extract_first_code_block(text) -> str:
		pattern = r"```(.+?)\n(.+?)```"
		match = re.search(pattern, text, re.DOTALL)
		if match:
			language = match.group(1)
			code = match.group(2)
			return code
		return ""

	# Example usage
	def parse(self, text: str) -> str:
		return self.__extract_first_code_block(text)
