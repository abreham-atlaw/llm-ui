import json
import unittest

from llmui.core.agent.directed.sections.debug.serializers.error_extraction_state_serializer import \
	ErrorExtractionStateSerializer
from llmui.core.agent.directed.sections.debug.states.error_extraction_state import ErrorExtractionState, Error


class ErrorExtractionStateSerializerTest(unittest.TestCase):

	def test_functionality(self):

		serializer = ErrorExtractionStateSerializer()

		state = ErrorExtractionState()
		state.errors = [
			Error(
				test_case=f"Test Case{i}",
				file_path="path/to/file",
				error="Test Error"
			)
			for i in range(5)
		]

		data = serializer.serialize(state)
		data_json = json.dumps(data)

		self.assertIsNotNone(data)
		self.assertIsNotNone(data_json)
