import typing

from llmui.core.agent.directed.lib.executor import I
from llmui.core.agent.directed.sections.debug.states.error_extraction_state import Error
from llmui.core.agent.directed.sections.implementation.executors.base_list_files_executor import BaseListFilesExecutor
from llmui.utils.format_utils import FormatUtils


class ListDebugRelevantFilesExecutor(BaseListFilesExecutor[typing.Tuple[Error, typing.List[str], typing.Dict[str, str], typing.Callable]]):

	def _prepare_prompt(self, arg: typing.Tuple[Error, typing.List[str], typing.Dict[str, str], typing.Callable]) -> str:

		error, docs, analysis, reader = arg

		return f"""
I got the following error when running a test case:
{FormatUtils.format_content(error.error)}


Here's the test case file({error.test_case}):
{error.file_path}

{FormatUtils.format_content(reader(error.file_path))}


Here's a documentation that might help:
{FormatUtils.format_docs(docs)}


Here are files on the project that might be relevant with their respective description:
{FormatUtils.generate_files_list(list(analysis.keys()), description=analysis)}


List the files that you need to see to solve the bug. Just make a numbered list of the file paths.
"""