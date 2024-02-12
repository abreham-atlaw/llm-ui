import os.path
import typing

import re

from llmui.core.agent.directed.lib.executor import LLMExecutor
from llmui.core.agent.directed.sections.implementation.executors.summarize_task_executor import SummarizeTaskExecutor
from llmui.utils.format_utils import FormatUtils


class FileImplementationExecutor(LLMExecutor[typing.Tuple[str, typing.List[str], str, str, str, typing.List[str], typing.Callable, typing.List[str]], str]):

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
Given the current content of the file:
// {file}
```
{read(file)}
```
"""
		return ""

	def _prepare_prompt(self, arg: typing.Tuple[str, typing.List[str], str, str, str, typing.List[str], typing.Callable, typing.List[str]]) -> str:
		context, tech_stack, root_path, file, file_task, dependencies, read, docs = arg
		prompt = f"""
Given the following tech stack:
{', '.join(tech_stack)}.

{'Given the following files:' if len(dependencies) > 0 else ''}
{self.__generate_dependencies_content(dependencies, read, root_path) if len(dependencies) > 0 else ''}

Given the following context:
{context}

{self.__generate_file_content(root_path, file, read)}

Given the following documentation:
{FormatUtils.format_docs(docs)}

Implement or modify the file {file} with the following task:
{file_task}

Just send the complete code for the file {file}. Don't add no comments unless you necessarily have to. Feel free to send the original code back if the file needs no modification.
Note: Make sure to leave any placeholder in the code. Use the provided context and documentation to fill in the values.
""".replace("\n\n\n\n","\n")
		return prompt

	def _prepare_output(self, output: str, arg:  typing.Tuple[str, typing.List[str], str, str, str, typing.List[str], typing.Callable, typing.List[str]]) -> str:
		return self.__extract_first_code_block(output)
