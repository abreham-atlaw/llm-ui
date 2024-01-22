import os.path
import typing

from llmui.core.agent.directed.lib.executor import LLMExecutor, I, O
from llmui.utils.format_utils import FormatUtils


class AnalyzeFileExecutor(LLMExecutor[
							typing.Tuple[str, typing.Callable, typing.List[str]],
							str
						]):

	def _prepare_prompt(self, arg: typing.Tuple[str, typing.Callable, typing.List[str]]) -> str:
		file_path, read, docs = arg
		return f"""
Given the following documentation:
{FormatUtils.format_docs(docs)}		

Analyze the following file: {os.path.basename(file_path)}:
```
{read(file_path)}
```

Give a very short description using a sentence or two of it's contents(classes, function, ...), the purpose of the file and so on.
"""

	def _prepare_output(self, output: str, arg: typing.Tuple[str, typing.Callable, typing.List[str]]) -> str:
		return output

