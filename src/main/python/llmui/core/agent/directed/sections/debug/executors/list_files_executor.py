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

Can you make a numbered list of files I should check to solve this issue? Use the format below:
1. path/to/file: descriptions for change
2. path/to/file2: descriptions for change

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
