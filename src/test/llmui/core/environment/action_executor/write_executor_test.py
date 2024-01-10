import os.path
import unittest

from llmui.config import PROJECT_PATH
from llmui.core.environment import LLMUIAction
from llmui.core.environment.action_executor import WriteExecutor


class WriteExecutorTest(unittest.TestCase):

	def test_functionality(self):
		executor = WriteExecutor(
			cwd=PROJECT_PATH
		)

		file = "tests/components/x.specs.ts"
		executor.execute(LLMUIAction(
			command="write",
			args=[
				file,
				"Test Content"
			]
		))

		self.assertTrue(os.path.exists(os.path.join(PROJECT_PATH, file)))