from lib.gai_client import Llama2Client
from llmui.config import GAI_URL, DOCS_EXTENSION
from lib.vectordb import VectorDB, ChromaVectorDB


class UtilsProviders:

	__vector_db = None
	__documentations = {}
	__analysis_db = None

	@staticmethod
	def provide_llama2_client() -> Llama2Client:
		return Llama2Client(GAI_URL)

	@staticmethod
	def provide_vectordb() -> VectorDB:
		return ChromaVectorDB()

	@staticmethod
	def provide_documentation(docs: str) -> 'Documentation':
		from llmui.core.agent.directed.lib.vectordb.documentation import Documentation
		if UtilsProviders.__documentations.get(docs) is None:
			UtilsProviders.__documentations[docs] = Documentation(docs, docs_ext=DOCS_EXTENSION)
		return UtilsProviders.__documentations[docs]

	@staticmethod
	def provide_analysis_db():
		from llmui.core.agent.directed.lib.vectordb.analysisdb import AnalysisDB
		from llmui.di.handler_providers import HandlerProviders
		if UtilsProviders.__analysis_db is None:
			UtilsProviders.__analysis_db = AnalysisDB(HandlerProviders.provide_analysis_handler())
		return UtilsProviders.__analysis_db
