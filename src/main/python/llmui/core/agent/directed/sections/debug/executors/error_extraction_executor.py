import typing

from llmui.core.agent.directed.lib.executor import LLMExecutor, I, O
from llmui.core.agent.directed.sections.common.executors.format_executor import FormatExecutor
from llmui.core.agent.directed.sections.debug.states.error_extraction_state import Error
from llmui.utils.format_utils import FormatUtils


class ErrorExtractionExecutor(LLMExecutor[str, typing.List[Error]]):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__format_executor = FormatExecutor(
			llm=self._llm,
			output_format="""
{
"0": {
		"file_path": "path/to/test/case/file",
		"case_name": "Test Case Name",
		"error": "Test Case Error",
		"stacktrace": "Test Case Stacktrace...",
		"extra": "Other Info.."
		
	},
"1": {
		"file_path": "path/to/second/test/case",
		"case_name": "Second Test Case Name",
		"error": "Second Test Case Error",
		"stacktrace": "Second Test Case Stacktrace...",
		"extra": "Other Info.."
		
	},
...
}
""")

	def _prepare_prompt(self, arg: str) -> str:
		return f"""
Given the following error list the test cases that failed with their respective filepath, error, stacktrace and other relevant important information(include any other information that is relevant to solving the issue.)

```
{arg}
```

Note: Create a numbered list of the test cases with the details.

If it's not a test case error just extract the error and stacktrace.
"""

	def _prepare_output(self, output: str, arg: I) -> O:
		output = self.__format_executor(output)

		errors = FormatUtils.extract_list_from_json_string(output)
		return [
			Error(
				file_path=error["file_path"],
				test_case=error["case_name"],
				error=f"""
Error: {error["error"]}


Stacktrace:\n{error["stacktrace"]}


Extra Information:\n {error["extra"]}
"""
			)
			for error in errors
		]
