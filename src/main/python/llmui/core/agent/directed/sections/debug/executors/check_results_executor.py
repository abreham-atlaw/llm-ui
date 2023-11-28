import typing

import re

from llmui.core.agent.directed.lib.executor import LLMExecutor


class CheckResultsExecutor(LLMExecutor[str, bool]):

	def _prepare_prompt(self, arg: str) -> str:
		return f"""
I just got this output when I run a docker file:
{arg}
Did it run successfully and passed all the testes? Format you answer in the following format:
{{
passed: 0 // 0 for fail and 1 for pass
}}
Use 0 if the test failed to run at all as well
"""

	@staticmethod
	def __extract_passed_value(json_string) -> bool:
		# Define the pattern to match the "passed" value
		pattern = r'"passed":\s*(\d)'

		# Search for the pattern in the JSON string
		match = re.search(pattern, json_string)

		if match:
			# Extract the matched value and convert it to a boolean
			passed_value = bool(int(match.group(1)))

			return passed_value
		else:
			# If the pattern is not found, return None or raise an exception
			raise Exception(f"Parsing Error: couldn't parse the string {json_string}")

	def _prepare_output(self, output: str, arg: str) -> bool:
		return self.__extract_passed_value(output)
