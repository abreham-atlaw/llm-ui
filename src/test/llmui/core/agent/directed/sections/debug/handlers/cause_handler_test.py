import json
import unittest

from llmui.config import EXTRAS_SAVE_PATH, ENVIRON_PATH
from llmui.core.agent.directed.sections.common.models import ProjectInfo
from llmui.core.agent.directed.sections.debug.handlers.cause_handler import CauseHandler, CauseHandlerArgs
from llmui.core.agent.directed.sections.debug.states.error_extraction_state import Error
from llmui.core.environment import LLMUIEnvironment
from llmui.di import LLMProviders


class CauseHandlerTest(unittest.TestCase):

	def test_functionality(self):
		environment = LLMUIEnvironment(
			environ_file=ENVIRON_PATH
		)

		with open(EXTRAS_SAVE_PATH, "r") as file:
			extras = json.load(file)

		handler = CauseHandler(LLMProviders.provide_default_llm())

		while not handler.internal_state.done:
			handler.handle(
				environment.state,
				CauseHandlerArgs(
					error=Error(
						error="Error: rest_framework.exceptions.ValidationError: {'first_name': [ErrorDetail(string='This field is required.', code='required')], 'last_name': [ErrorDetail(string='This field is required.', code='required')]}'\n\n\nStacktrace:\nTraceback (most recent call last):\n  File \"/code/apps/authentication/tests/test_signup_view.py\", line 29, in test_invalid_signup\n    serializer.is_valid(raise_exception=True)\n  File \"/usr/local/lib/python3.11/site-packages/rest_framework/serializers.py\", line 235, in is_valid\n    raise ValidationError(self.errors)\n\n\nExtra Information:\n This test case is testing the validation of the signup view. It is expected to raise a ValidationError when the first_name and last_name fields are not provided.\n",
						test_case="test_invalid_signup",
						file_path="apps/authentication/tests/test_signup_view.py"
					),
					project_info=ProjectInfo(
						task=None,
						tech_stack=extras["tech_stack"],
						ignored_files=extras["ignored_files"],
						docs=extras["docs"]
					)
				)
			)

		self.assertIsNotNone(handler.internal_state.cause)

