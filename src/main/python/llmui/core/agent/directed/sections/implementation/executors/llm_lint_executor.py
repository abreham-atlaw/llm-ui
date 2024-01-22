import typing

from llmui.core.agent.directed.lib.executor import LLMExecutor
from llmui.core.agent.directed.sections.common.executors.format_executor import FormatExecutor
from llmui.utils.format_utils import FormatUtils


class LLMLintExecutor(LLMExecutor[typing.Tuple[str, str, typing.List[str]], typing.List[str]]):

	def _prepare_prompt(self, arg: typing.Tuple[str, str, typing.List[str]]) -> str:
		file, content, tech_stack = arg
		return f"""
Can you check if the following file, {file}, has any errors:
```
{content}
```

I'm using {', '.join(tech_stack)}.

List the errors and solution in the following format:
{{
"0": first_error,
"1": second_error,
"2": third_error
...
}}
Leave {{}} if there are no errors.
"""

	def _prepare_output(self, output: str, arg: typing.Tuple[str, str, typing.List[str]]) -> typing.List[str]:
		return FormatUtils.extract_list_from_json_string(output)
