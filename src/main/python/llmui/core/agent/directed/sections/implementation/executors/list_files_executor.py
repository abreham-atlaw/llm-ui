import typing

from enum import Enum

from llmui.core.agent.directed.lib.executor import LLMExecutor
from llmui.core.agent.directed.sections.common.executors.format_executor import FormatExecutor
from llmui.core.agent.directed.sections.implementation.executors.base_list_files_executor import BaseListFilesExecutor
from llmui.utils.format_utils import FormatUtils


class ListFilesExecutor(BaseListFilesExecutor[typing.Tuple[str, typing.List[str], typing.List[str], typing.Dict[str, str], typing.List[str]]]):

	def __get_implemented_files(self, files: typing.Dict[str, str]) -> str:
		if len(files) == 0:
			return ""
		return f"""
Here are a list of relevant files currently on the project:
{FormatUtils.generate_files_list(list(files.keys()), description=files)}
"""

	def _prepare_prompt(self, arg: typing.Tuple[str, typing.List[str], typing.List[str], typing.Dict[str, str], typing.List[str]]) -> str:
		task, tech_stack, files, analysis, docs = arg
		return f"""
I would like it if you could help me on a project I was working on. Could you list the files(code, ignore assets) I have to work on?
The project uses {', '.join(tech_stack)}.

I wanted to accomplish the following task.
{task}

Can you make a list of files(their paths, feel free to create new files) with what I need to do on the file?
Make it as detailed as possible (include classes, functions to be implemented). So that it can be independently passed to the engineer to implement.
Only include files relevant to the task

{self.__get_implemented_files(analysis)}

Here's a relevant section of the doc: 
{FormatUtils.format_docs(docs)}

Note: Only include files(not folders) & Only list files(code) that need to be modified or created to achieve the given task ignoring assets.
Minimize the number of files to modify or create.
You should also include only editable files not images, audio, ...
"""
