import typing

from llmui.core.agent.directed.lib.executor import LLMExecutor, I
from llmui.core.agent.directed.sections.implementation.executors.base_list_files_executor import BaseListFilesExecutor
from llmui.utils.format_utils import FormatUtils


class ListDebugFilesExecutor(BaseListFilesExecutor[typing.Tuple[str, typing.List[str], typing.List[str], typing.Dict[str, str], typing.List[str]]]):

	def _prepare_prompt(self, arg: typing.Tuple[str, typing.List[str], typing.List[str], typing.Dict[str, str], typing.List[str]]) -> str:
		task, tech_stack, files, analysis, docs = arg
		return f"""
I would like it if you could help me on a project I was working on. Could you list the files(code, ignore assets) I have to work on?
The project uses {', '.join(tech_stack)}.

I tried running the test but it failed with the error below:
{task}

Can you make a list of files(their paths, feel free to create new files) with what I need to do on the file to fix the issue above?
Make it as detailed as possible(include classes, functions to be implemented).

{FormatUtils.generate_files_list(list(analysis.keys()), analysis)}

Here's a relevant section of the doc: 
{FormatUtils.format_docs(docs)}

Note: Only include files(not folders) & Only list files(code) that need to be modified or created to achieve the given task ignoring assets.
Minimize the number of files to modify or create.
You should also include only editable files not images, audio, ...
"""
