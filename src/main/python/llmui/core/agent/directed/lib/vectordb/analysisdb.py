import typing

from llmui.config import ANALYSIS_FILES_SIZE
from llmui.core.agent.directed.sections.init.handlers.analysis_handler import AnalysisHandler
from llmui.di.utils_providers import UtilsProviders


class AnalysisDB:

	def __init__(self, handler: AnalysisHandler, delimiter=":\n\n"):
		self.__handler = handler
		self.__db = UtilsProviders.provide_vectordb()
		self.__files_db = UtilsProviders.provide_vectordb()
		self.__dirs_db = UtilsProviders.provide_vectordb()
		self.__delimiter = delimiter

	def __is_filetype(self, file, filetype) -> bool:
		if filetype is None:
			return True
		return self.__handler.internal_state.types[file] == filetype

	def refresh(self):
		self.__db, self.__files_db, self.__dirs_db = [UtilsProviders.provide_vectordb() for _ in range(3)]
		for db, file_type in zip([self.__db, self.__files_db, self.__dirs_db], [None, AnalysisHandler.FileType.file, AnalysisHandler.FileType.dir]):
			db.add(
				documents=[
					f"{file}{self.__delimiter}{analysis}"
					for file, analysis in self.__handler.internal_state.analysis.items()
					if self.__is_filetype(file, file_type)
				]
			)

	def __construct_result(self, results: typing.List[str]) -> typing.Dict[str, str]:
		analysis = {}
		for result in results:
			result_split = result.split(self.__delimiter)
			analysis[result_split[0]] = self.__delimiter.join(result_split[1:])
		return analysis

	def get_analysis(self, query: str, num_files=ANALYSIS_FILES_SIZE, file_type=None) -> typing.Dict[str, str]:
		self.refresh()  # TODO: Make this conditional on if hash of analysis handler.state has changed

		db = self.__db
		if file_type == AnalysisHandler.FileType.file:
			db = self.__files_db
		elif file_type == AnalysisHandler.FileType.dir:
			db = self.__dirs_db
		results = db.query(query, num_results=num_files)
		return self.__construct_result(results)

