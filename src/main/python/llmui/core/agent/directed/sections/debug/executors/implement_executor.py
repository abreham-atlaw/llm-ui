import typing

from llmui.core.agent.directed.lib.executor import LLMExecutor, I, O
from llmui.utils.format_utils import FormatUtils


class ImplementExecutor(LLMExecutor[typing.Tuple[str, str, typing.Callable], str]):

	def _prepare_prompt(self, arg: typing.Tuple[str, str, typing.Callable]) -> str:
		file_path, changes, read = arg
		return f"""
I have the following file:
//{file_path}
```
{read(file_path)}
```
I wanted to make the following changes to it:
{changes}

Can you make those changes and return the complete code. 
"""

	def _prepare_output(self, output: str, arg: typing.Tuple[str, str]) -> str:
		return FormatUtils.extract_first_code_block(output)