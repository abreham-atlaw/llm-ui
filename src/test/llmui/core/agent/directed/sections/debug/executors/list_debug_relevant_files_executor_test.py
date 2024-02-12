import json
import unittest

from llmui.config import ENVIRON_PATH, EXTRAS_SAVE_PATH
from llmui.core.agent.directed.sections.debug.executors.list_debug_relevant_files_executor import \
	ListDebugRelevantFilesExecutor
from llmui.core.agent.directed.sections.debug.states.error_extraction_state import Error
from llmui.core.agent.directed.sections.init.handlers.analysis_handler import AnalysisHandler
from llmui.core.environment import LLMUIEnvironment
from llmui.di import LLMProviders
from llmui.di.utils_providers import UtilsProviders


class ListDebugRelevantFilesExecutorTest(unittest.TestCase):

	def test_functionality(self):
		environment = LLMUIEnvironment(
			environ_file=ENVIRON_PATH
		)
		with open(EXTRAS_SAVE_PATH, "r") as file:
			extras = json.load(file)

		executor = ListDebugRelevantFilesExecutor(LLMProviders.provide_default_llm())

		error = Error(
			error="Error: rest_framework.exceptions.ValidationError: {'first_name': [ErrorDetail(string='This field is required.', code='required')], 'last_name': [ErrorDetail(string='This field is required.', code='required')]}'\n\n\nStacktrace:\nTraceback (most recent call last):\n  File \"/code/apps/authentication/tests/test_signup_view.py\", line 29, in test_invalid_signup\n    serializer.is_valid(raise_exception=True)\n  File \"/usr/local/lib/python3.11/site-packages/rest_framework/serializers.py\", line 235, in is_valid\n    raise ValidationError(self.errors)\n\n\nExtra Information:\n This test case is testing the validation of the signup view. It is expected to raise a ValidationError when the first_name and last_name fields are not provided.\n",
			test_case="test_invalid_signup",
			file_path="apps/authentication/tests/test_signup_view.py"
		)
		docs = UtilsProviders.provide_documentation(extras["docs"]).search(error.error, num_results=2)
		files = executor((
			error,
			docs,
			UtilsProviders.provide_analysis_db().get_analysis(error.error, num_files=20, file_type=AnalysisHandler.FileType.file),
			environment.state.read_content
		))

		self.assertIsNotNone(files)
