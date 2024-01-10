import os.path

from llmui.config import ANALYSIS_SAVE_PATH
from llmui.core.agent.directed.sections.init.handlers.analysis_handler import AnalysisHandler
from llmui.di import LLMProviders


class HandlerProviders:

	__analysis_handler = None

	@staticmethod
	def provide_analysis_handler():
		if HandlerProviders.__analysis_handler is None:
			if os.path.exists(ANALYSIS_SAVE_PATH):
				HandlerProviders.__analysis_handler = AnalysisHandler.load_handler(
					ANALYSIS_SAVE_PATH,
					llm=LLMProviders.provide_default_llm(),
					auto_save_path=ANALYSIS_SAVE_PATH
				)
			else:
				HandlerProviders.__analysis_handler = AnalysisHandler(LLMProviders.provide_default_llm(), auto_save_path=ANALYSIS_SAVE_PATH)
		return HandlerProviders.__analysis_handler
