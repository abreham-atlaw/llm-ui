import os
import typing

from llmui.core.agent.directed.lib.executor import LLMExecutor, I, O


class AnalyzeDirExecutor(LLMExecutor[
							typing.Tuple[str, str, typing.Dict[str, str]],
							str
						]):

	@staticmethod
	def __prepare_files(project_path, dir_path, files_analysis) -> str:
		return "\n\n".join([
			f"""
{filename}
{files_analysis.get(os.path.join(dir_path, filename), '').strip()}
"""
			for filename in os.listdir(os.path.join(project_path, dir_path))
		])

	def _prepare_prompt(self, arg: typing.Tuple[str, str, typing.Dict[str, str]]) -> str:
		project_path, dir_path, files_analysis = arg
		return f"""
I have the directory {dir_path} with the following files:

{self.__prepare_files(project_path, dir_path, files_analysis)}

Write an overall description of the folder and it's function. Don't include descriptions of the files in it I only need a short description of the purpose of the folder
""".strip()

	def _prepare_output(self, output: str, arg: typing.Tuple[str, str, typing.Dict[str, str]]) -> str:
		return output
