import typing

from llmui.core.agent.directed.lib.executor import LLMExecutor, I, O
from llmui.core.agent.directed.sections.common.executors.format_executor import FormatExecutor
from llmui.utils.format_utils import FormatUtils


class ContentCheckExecutor(LLMExecutor[typing.Tuple[str, str, str], bool]):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__format_executor = FormatExecutor(
			llm=self._llm,
			output_format="""
{
complete": 0 // 0 if there's anything missing; 1 otherwise;
}
"""
		)


	def _prepare_prompt(self, arg: typing.Tuple[str, str, str]) -> str:
		original, task, new = arg
# 		return f"""
# I originally have the file below:
# ```
# {original}
# ```
#
# I wanted to make the following change to it:
# - {task}
#
# Here's the complete content of the new file:
# ```
# {new}
# ```
# Is there anything missing from the new file that is present in the old file?(Even those irrelevant to the task). In other words in the following a complete file.
#
# Format your answer in the following way:
# {{
# "complete": 0 // 0 if there's anything missing; 1 otherwise;
# }}
# """
		return f"""
Given the original code:
```
{original}
```

And the modified code:
```
{new}
```

The task was to:
- {task}

Please analyze and determine if the modified code is a complete solution or just a snippet.
"""

	def _prepare_output(self, output: str, arg: typing.Tuple[str, str, str]) -> bool:
		output = self.__format_executor(output)
		output = FormatUtils.extract_json_from_string(output).get("complete", 0)
		return output == 1
