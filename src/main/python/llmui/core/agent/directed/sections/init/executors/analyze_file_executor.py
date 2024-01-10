import os.path
import typing

from llmui.core.agent.directed.lib.executor import LLMExecutor, I, O


class AnalyzeFileExecutor(LLMExecutor[
							typing.Tuple[str, typing.Callable],
							str
						]):

	def _prepare_prompt(self, arg: typing.Tuple[str, typing.Callable]) -> str:
		file_path, read = arg
		return f"""
Analyze the following file: {os.path.basename(file_path)}:
```
{read(file_path)}
```

Give a very short description using a sentence or two of it's contents(classes, function, ...), the purpose of the file and so on.
"""

	def _prepare_output(self, output: str, arg: typing.Tuple[str, typing.Callable]) -> str:
		return output

