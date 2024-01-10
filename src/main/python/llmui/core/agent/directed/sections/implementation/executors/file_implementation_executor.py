import os.path
import typing

import re

from llmui.core.agent.directed.lib.executor import LLMExecutor
from llmui.core.agent.directed.sections.implementation.executors.summarize_task_executor import SummarizeTaskExecutor


class FileImplementationExecutor(LLMExecutor[typing.Tuple[str, typing.List[str], str, str, str, typing.List[str], typing.Callable], str]):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__summarize_executor = SummarizeTaskExecutor(self._llm)

	@staticmethod
	def __extract_first_code_block(text) -> str:
		pattern = r"```(.+?)\n(.+?)```"
		match = re.search(pattern, text, re.DOTALL)
		if match:
			language = match.group(1)
			code = match.group(2)
			return code
		return ""

	@staticmethod
	def __generate_dependencies_content(dependencies: typing.List[str], read: typing.Callable, root_path: str) -> str:
		return "\n\n".join([
			f"""
//{file}
```
{read(file)}
```
"""
			for file in dependencies
			if os.path.exists(os.path.join(root_path, file))
		])

	@staticmethod
	def __generate_file_content(root_path, file, read):
		if os.path.exists(os.path.join(root_path, file)):
			return f"""
The current content of the file, {file}, is:
```
{read(file)}
```
"""
		return f"""
The file, {file}, has not been implemented yet. 
"""

	def _prepare_prompt(self, arg: typing.Tuple[str, typing.List[str], str, str, str, typing.List[str], typing.Callable]) -> str:
		project_task, tech_stack, root_path, file, file_task, dependencies, read = arg
		prompt = f"""
I would like it if you could help me on an app I was working on. Can you help me implement a file?
I'm using {', '.join(tech_stack)} to build the project.

The task on the project is:
{project_task}

I have the following files:
{self.__generate_dependencies_content(dependencies, read, root_path)}

{self.__generate_file_content(root_path, file, read)}

Implement or modify the file {file} with the following task:
{file_task}

Just send the complete code for the file {file}. Don't add no comments unless you necessarily have to. Feel free to send "No changes required" as a comment it the file needs no modification.
"""
		# prompt = self.__summarize_executor(prompt)
		return prompt

	def _prepare_output(self, output: str, arg:  typing.Tuple[str, typing.List[str], str, str, str, typing.List[str], typing.Callable]) -> str:
		return self.__extract_first_code_block(output)
