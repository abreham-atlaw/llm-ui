import unittest

from llmui.core.agent.directed.lib.vectordb.analysisdb import AnalysisDB
from llmui.core.agent.directed.sections.init.handlers.analysis_handler import AnalysisHandler
from llmui.di.utils_providers import UtilsProviders
from llmui.utils.format_utils import FormatUtils


class AnalysisDBTest(unittest.TestCase):

	def test_functionality(self):
		db: AnalysisDB = UtilsProviders.provide_analysis_db()
		files = db.get_analysis("""
Error: rest_framework.exceptions.ValidationError: {'first_name': [ErrorDetail(string='This field is required.', code='required')], 'last_name': [ErrorDetail(string='This field is required.', code='required')]}'


Stacktrace:
Traceback (most recent call last):
  File \"/code/apps/authentication/tests/test_signup_view.py\", line 29, in test_invalid_signup
    serializer.is_valid(raise_exception=True)
  File \"/usr/local/lib/python3.11/site-packages/rest_framework/serializers.py\", line 235, in is_valid
    raise ValidationError(self.errors)


Extra Information:
 This test case is testing the validation of the signup view. It is expected to raise a ValidationError when the first_name and last_name fields are not provided.
""", num_files=20, file_type=AnalysisHandler.FileType.file)
		analysis = FormatUtils.generate_files_list(list(files.keys()), description=files)
		self.assertIsNotNone(files)

