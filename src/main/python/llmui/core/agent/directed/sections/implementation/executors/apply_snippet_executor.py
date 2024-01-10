import typing

from llmui.core.agent.directed.lib.executor import LLMExecutor, I, O
from llmui.utils.format_utils import FormatUtils


class ApplySnippetExecutor(LLMExecutor[typing.Tuple[str, str], str]):

	def _prepare_prompt(self, arg: typing.Tuple[str, str]) -> str:
		original, snippet = arg
		return f"""
I have the file below:
```
{original}
```

Can you apply the snippet below to the file:
```
{snippet}
```

Note: Write the whole file with the changes included.
"""

	def _prepare_output(self, output: str, arg: typing.Tuple[str, str]) -> str:
		return FormatUtils.extract_first_code_block(output)
