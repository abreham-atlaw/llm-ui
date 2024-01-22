import unittest

from llmui.core.agent.directed.lib.vectordb.analysisdb import AnalysisDB
from llmui.di.utils_providers import UtilsProviders


class AnalysisDBTest(unittest.TestCase):

	def test_functionality(self):
		db: AnalysisDB = UtilsProviders.provide_analysis_db()
		files = db.get_analysis("Implement a request class for fetching products from the backend", num_files=10)

		self.assertIsNotNone(files)

