import typing

from llmui.core.agent.directed.lib.executor import LLMExecutor
from llmui.core.agent.directed.sections.debug.states.error_extraction_state import Error
from llmui.utils.format_utils import FormatUtils


class CauseExecutor(LLMExecutor[typing.Tuple[Error, typing.List[str], typing.List[str], typing.Callable], str]):

	def _prepare_prompt(self, arg: typing.Tuple[Error, typing.List[str], typing.List[str], typing.Callable]) -> str:
		error, files, docs, reader = arg
		return f"""
Find the bug given the information below.

Given the following files:

{FormatUtils.generate_files_list(
			files_list=files,
			description={
				file: FormatUtils.format_content(reader(file))
				for file in files
			}
		)}
		

Given the following test file:

{error.file_path}
{FormatUtils.format_content(reader(error.file_path))}

Given the following documentation:
{FormatUtils.format_docs(docs)}

And given the error caused below when running the test({error.test_case}):
{FormatUtils.format_content(error.error)}

What is the bug? Write a report on the bug.
"""

	def _prepare_output(self, output: str, arg: typing.Tuple[Error, typing.List[str], typing.List[str], typing.Callable]) -> str:
		return output
