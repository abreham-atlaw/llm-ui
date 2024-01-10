import typing

import re

from llmui.core.agent.directed.lib.executor import LLMExecutor, I, O
from llmui.utils.format_utils import FormatUtils


class ListFilesExecutor(LLMExecutor[typing.Tuple[str, str, typing.Callable], typing.List[str]]):

	def _prepare_prompt(self, arg: typing.Tuple[str, str, typing.Callable]) -> str:
		path, message, read = arg

		return f"""
I have the following project:
{FormatUtils.tree(path)}
I'm running the dockerfile:
```Docker
{read("Dockerfile")}
```
I tried running the test but it failed with the error:
"{message}"

Can you make a list of files(their paths, feel free to create new files) with what I need to do on the file to fix the issue above?
Make it as detailed as possible(include classes, functions to be implemented).
"""

	def _prepare_output(self, output: str, arg: typing.Tuple[str, str, typing.Callable]) -> typing.List[str]:
		text = output.replace("*", "").replace("`", "")
		pattern = r'\d+\. (\S+): (.+)'
		matches = re.findall(pattern, text)

		result = []
		for match in matches:
			path, description = match
			result.append(path)

		return result
