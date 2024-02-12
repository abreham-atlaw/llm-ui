import typing

from llmui.core.agent.directed.lib.executor import LLMExecutor, I, O
from llmui.core.agent.directed.sections.implementation.executors.base_list_files_executor import BaseListFilesExecutor
from llmui.utils.format_utils import FormatUtils


class ListTestFilesExecutor(BaseListFilesExecutor[typing.Tuple[typing.List[str], typing.List[str], typing.Dict[str, str], str]]):

	def _prepare_prompt(self, arg: typing.Tuple[typing.List[str], typing.List[str], typing.Dict[str, str], str]) -> str:
		docs, files, analysis, task = arg
		return f"""
Considering the following documentation List the test files I need to implement:
{FormatUtils.format_docs(docs)}

And consider the following task:
{task}

Here is a list of implemented relevant files to this task:
{FormatUtils.generate_files_list(files, description=analysis)}

Just make a numbered list of the test files I should implement or modify. Drop files I don't need to work on. 
List the test files with with a brief task to perform on the file.
"""
