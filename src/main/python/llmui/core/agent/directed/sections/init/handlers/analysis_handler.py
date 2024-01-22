import typing
from typing import Optional

import os.path
from dataclasses import dataclass
from hashlib import md5

from llmui.core.agent.directed.lib.handler import Handler
from llmui.core.agent.directed.sections.common.models import ProjectInfo
from llmui.core.agent.directed.sections.init.executors.analyze_dir_executor import AnalyzeDirExecutor
from llmui.core.agent.directed.sections.init.executors.analyze_file_executor import AnalyzeFileExecutor
from llmui.core.agent.directed.sections.init.states.analyze_project_state import AnalyzeProjectState
from llmui.core.environment import LLMUIState, LLMUIAction
from llmui.di.utils_providers import UtilsProviders


@dataclass
class AnalysisHandlerArgs:
	project_info: ProjectInfo


class AnalysisHandler(Handler[AnalyzeProjectState, AnalysisHandlerArgs]):

	class FileType:
		file = 0
		dir = 1

	INTERNAL_STATE_CLS = AnalyzeProjectState

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__analyze_file_executor = AnalyzeFileExecutor(self._llm)
		self.__analyze_dir_executor = AnalyzeDirExecutor(self._llm)

	def _init_internal_state(self) -> AnalyzeProjectState:
		return AnalyzeProjectState(
			analysis={},
			analysis_sig={},
			types={}
		)

	def __hash(self, content: str) -> str:
		return md5(content.encode("utf-8")).hexdigest()

	def __get_dir_content(self, path) -> str:
		return "\n".join([
			f"{filename}:{self.__get_signature(os.path.join(path, filename))}"
			for filename in os.listdir(path)
		])

	def __get_signature(self, path: str) -> str:
		if os.path.isdir(path):
			content = self.__get_dir_content(path)
		else:
			with open(path, "r", encoding='utf-8', errors='ignore') as fs:
				content = fs.read()
		return self.__hash(content)

	def __register_analysis(self, path: str):
		self.internal_state.analysis_sig[path] = self.__get_signature(path)

	def __skip_analysis(self, path: str):
		old_signature = self.internal_state.analysis_sig.get(path)
		new_signature = self.__get_signature(path)
		return old_signature == new_signature

	@staticmethod
	def __get_docs(file: str, reader: typing.Callable, docs: str) -> typing.List[str]:
		return UtilsProviders.provide_documentation(docs).search(
			f"""
// {file}
{reader(file)}
""".strip(),
			num_results=1
		)

	def __analyze(self, state: LLMUIState, dir_path: str, project_info: ProjectInfo):
		for file in state.listdir(dir_path):

			file_path = os.path.join(dir_path, file)
			if file_path.startswith("./"):
				file_path = file_path[2:]

			if file_path in project_info.ignored_files or self.__skip_analysis(file_path):
				continue

			print(f"[+]Analyzing {file_path}...")

			if os.path.isdir(os.path.join(state.root_path, file_path)):
				self.__analyze(state, file_path, project_info)
				self.internal_state.analysis[file_path] = self.__analyze_dir_executor((
					state.root_path,
					file_path,
					self.internal_state.analysis
				))
				self.internal_state.types[file_path] = AnalysisHandler.FileType.dir
			else:
				self.internal_state.analysis[file_path] = self.__analyze_file_executor((
					file_path,
					state.read_content,
					self.__get_docs(file_path, state.read_content, project_info.docs)
				))
				self.internal_state.types[file_path] = AnalysisHandler.FileType.file
			self.__register_analysis(file_path)
			self._auto_save()

	def _handle(self, state: LLMUIState, args: AnalysisHandlerArgs) -> Optional[LLMUIAction]:
		print("[+]Analyzing Project...")
		if self.internal_state.analysis is None:
			self.internal_state.analysis = {}

		self.__analyze(
			state,
			".",
			args.project_info
		)
		return None
