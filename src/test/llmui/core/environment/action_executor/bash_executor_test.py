import unittest

from llmui.core.environment import LLMUIAction
from llmui.core.environment.action_executor.bash_executor import BashExecutor


class BashExecutorTest(unittest.TestCase):

	def __get_pwd(self, executor):
		return executor.execute(LLMUIAction(
			command="bash",
			args=["pwd"]
		))

	def test_cd(self):
		CWD = "/home/abreham/Projects/TeamProjects/LLM-UI/temp/projects/orbit/web"
		NEW_CWD = "/home/abreham/Projects/TeamProjects/LLM-UI/temp/projects/orbit/web/orbit-website"
		executor = BashExecutor(cwd=CWD)
		pwd = self.__get_pwd(executor)
		self.assertEqual(pwd, CWD)
		executor.execute(LLMUIAction(
			command="bash",
			args=["cd", NEW_CWD]
		))
		new_pwd = self.__get_pwd(executor)
		self.assertEqual(new_pwd, NEW_CWD)
